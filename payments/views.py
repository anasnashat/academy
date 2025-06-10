import stripe
import json
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse, HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST
from django.conf import settings
from django.contrib import messages
from django.urls import reverse
from courses.models import Course, Purchase

# Set Stripe API key
stripe.api_key = settings.STRIPE_SECRET_KEY

@login_required
def create_payment_intent(request):
    """Create a Stripe Payment Intent for course purchase"""
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            course_id = data.get('course_id')
            
            course = get_object_or_404(Course, id=course_id)
            
            # Check if user already purchased this course
            if Purchase.objects.filter(user=request.user, course=course, is_completed=True).exists():
                return JsonResponse({
                    'error': 'You have already purchased this course'
                }, status=400)
            
            # Convert price to cents (Stripe expects amounts in cents)
            amount = int(course.price * 100)
            
            # Create payment intent
            intent = stripe.PaymentIntent.create(
                amount=amount,
                currency='usd',
                metadata={
                    'course_id': course.id,
                    'user_id': request.user.id,
                    'course_title': course.title
                }
            )
            
            # Create or update purchase record
            purchase, created = Purchase.objects.get_or_create(
                user=request.user,
                course=course,
                defaults={
                    'stripe_payment_intent_id': intent.id,
                    'amount_paid': course.price,
                    'is_completed': False
                }
            )
            
            if not created:
                purchase.stripe_payment_intent_id = intent.id
                purchase.save()
            
            return JsonResponse({
                'client_secret': intent.client_secret,
                'amount': amount,
                'currency': 'usd'
            })
            
        except Exception as e:
            return JsonResponse({
                'error': str(e)
            }, status=400)
    
    return JsonResponse({'error': 'Invalid request method'}, status=405)

@login_required
def checkout(request, course_id):
    """Display checkout page for course"""
    course = get_object_or_404(Course, id=course_id)
    
    # Check if user already purchased this course
    if Purchase.objects.filter(user=request.user, course=course, is_completed=True).exists():
        messages.info(request, 'You have already purchased this course.')
        return redirect('course_detail', course_id=course.id)
    
    context = {
        'course': course,
        'stripe_publishable_key': settings.STRIPE_PUBLISHABLE_KEY,
    }
    
    return render(request, 'payments/checkout.html', context)

@login_required
def payment_success(request):
    """Handle successful payment"""
    payment_intent_id = request.GET.get('payment_intent')
    
    if payment_intent_id:
        try:
            # Retrieve the payment intent from Stripe
            intent = stripe.PaymentIntent.retrieve(payment_intent_id)
            
            if intent.status == 'succeeded':
                # Find and update the purchase
                purchase = Purchase.objects.filter(
                    stripe_payment_intent_id=payment_intent_id
                ).first()
                
                if purchase:
                    purchase.is_completed = True
                    purchase.save()
                    
                    messages.success(request, f'Payment successful! You now have access to "{purchase.course.title}".')
                    return redirect('course_learn', course_id=purchase.course.id)
        
        except Exception as e:
            messages.error(request, 'There was an error processing your payment. Please contact support.')
    
    return redirect('course_list')

@login_required
def payment_cancel(request):
    """Handle cancelled payment"""
    messages.warning(request, 'Payment was cancelled. You can try again anytime.')
    return redirect('course_list')

@csrf_exempt
def stripe_webhook(request):
    """Handle Stripe webhooks"""
    payload = request.body
    sig_header = request.META.get('HTTP_STRIPE_SIGNATURE')
    endpoint_secret = settings.STRIPE_WEBHOOK_SECRET
    
    try:
        event = stripe.Webhook.construct_event(
            payload, sig_header, endpoint_secret
        )
    except ValueError:
        # Invalid payload
        return HttpResponse(status=400)
    except stripe.error.SignatureVerificationError:
        # Invalid signature
        return HttpResponse(status=400)
    
    # Handle the event
    if event['type'] == 'payment_intent.succeeded':
        payment_intent = event['data']['object']
        
        # Update purchase status
        try:
            purchase = Purchase.objects.get(
                stripe_payment_intent_id=payment_intent['id']
            )
            purchase.is_completed = True
            purchase.save()
        except Purchase.DoesNotExist:
            pass
    
    elif event['type'] == 'payment_intent.payment_failed':
        payment_intent = event['data']['object']
        
        # Handle failed payment
        try:
            purchase = Purchase.objects.get(
                stripe_payment_intent_id=payment_intent['id']
            )
            # You can add additional logic here for failed payments
            # For example, send an email notification
        except Purchase.DoesNotExist:
            pass
    
    return HttpResponse(status=200)
