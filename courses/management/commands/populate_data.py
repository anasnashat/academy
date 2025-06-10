from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from courses.models import Category, Course, Section, Lesson, Purchase, LessonProgress, CourseReview, Comment
from django.utils.text import slugify
import random

class Command(BaseCommand):
    help = 'Populate the database with sample course data'

    def handle(self, *args, **options):
        self.stdout.write('Creating sample data...')
        
        # Create superuser if doesn't exist
        if not User.objects.filter(username='admin').exists():
            admin = User.objects.create_superuser(
                username='admin',
                email='admin@academy.com',
                password='admin123',
                first_name='Admin',
                last_name='User'
            )
            self.stdout.write(self.style.SUCCESS('Created admin user: admin/admin123'))
        else:
            admin = User.objects.get(username='admin')

        # Create some instructors
        instructors = []
        instructor_data = [
            {'username': 'john_doe', 'first_name': 'John', 'last_name': 'Doe', 'email': 'john@academy.com'},
            {'username': 'jane_smith', 'first_name': 'Jane', 'last_name': 'Smith', 'email': 'jane@academy.com'},
            {'username': 'mike_wilson', 'first_name': 'Mike', 'last_name': 'Wilson', 'email': 'mike@academy.com'},
        ]
        
        for data in instructor_data:
            instructor, created = User.objects.get_or_create(
                username=data['username'],
                defaults={
                    'first_name': data['first_name'],
                    'last_name': data['last_name'],
                    'email': data['email'],
                    'is_staff': True
                }
            )
            if created:
                instructor.set_password('instructor123')
                instructor.save()
            instructors.append(instructor)

        # Create categories
        categories_data = [
            {
                'name': 'Web Development',
                'name_ar': 'تطوير الويب',
                'description': 'Learn modern web development technologies',
                'description_ar': 'تعلم تقنيات تطوير الويب الحديثة',
                'icon': 'fas fa-code'
            },
            {
                'name': 'Data Science',
                'name_ar': 'علم البيانات',
                'description': 'Master data analysis and machine learning',
                'description_ar': 'إتقان تحليل البيانات والتعلم الآلي',
                'icon': 'fas fa-chart-bar'
            },
            {
                'name': 'Mobile Development',
                'name_ar': 'تطوير الجوال',
                'description': 'Build native and cross-platform mobile apps',
                'description_ar': 'بناء تطبيقات الجوال الأصلية ومتعددة المنصات',
                'icon': 'fas fa-mobile-alt'
            },
            {
                'name': 'DevOps',
                'name_ar': 'ديف أوبس',
                'description': 'Learn deployment and infrastructure management',
                'description_ar': 'تعلم النشر وإدارة البنية التحتية',
                'icon': 'fas fa-server'
            }
        ]

        categories = []
        for cat_data in categories_data:
            category, created = Category.objects.get_or_create(
                name=cat_data['name'],
                defaults={
                    'name_ar': cat_data['name_ar'],
                    'slug': slugify(cat_data['name']),
                    'description': cat_data['description'],
                    'description_ar': cat_data['description_ar'],
                    'icon': cat_data['icon']
                }
            )
            categories.append(category)

        # Create courses
        courses_data = [
            {
                'title': 'Complete Django Web Development',
                'title_ar': 'تطوير الويب الكامل باستخدام Django',
                'category': categories[0],  # Web Development
                'instructor': instructors[0],
                'description': 'Learn to build full-stack web applications with Django framework. This comprehensive course covers everything from basic concepts to advanced topics like REST APIs, authentication, and deployment.',
                'description_ar': 'تعلم بناء تطبيقات الويب الكاملة باستخدام إطار عمل Django. هذه الدورة الشاملة تغطي كل شيء من المفاهيم الأساسية إلى المواضيع المتقدمة مثل REST APIs والمصادقة والنشر.',
                'short_description': 'Master Django framework and build powerful web applications',
                'short_description_ar': 'إتقان إطار عمل Django وبناء تطبيقات ويب قوية',
                'price': 99.99,
                'difficulty_level': 'intermediate',
                'duration_weeks': 12,
                'requirements': 'Basic Python knowledge\nHTML/CSS fundamentals\nDatabase concepts',
                'requirements_ar': 'معرفة أساسية بـ Python\nأساسيات HTML/CSS\nمفاهيم قواعد البيانات',
                'what_you_learn': 'Build full-stack web applications\nDjango models, views, and templates\nUser authentication and authorization\nREST API development\nDeployment strategies',
                'what_you_learn_ar': 'بناء تطبيقات ويب كاملة\nنماذج وعروض وقوالب Django\nمصادقة المستخدمين والتخويل\nتطوير REST API\nاستراتيجيات النشر',
                'is_featured': True
            },
            {
                'title': 'React.js Frontend Development',
                'title_ar': 'تطوير الواجهات الأمامية باستخدام React.js',
                'category': categories[0],  # Web Development
                'instructor': instructors[1],
                'description': 'Master React.js and modern frontend development. Build interactive user interfaces with hooks, context, and state management.',
                'description_ar': 'إتقان React.js وتطوير الواجهات الأمامية الحديثة. بناء واجهات مستخدم تفاعلية باستخدام hooks وcontext وإدارة الحالة.',
                'short_description': 'Build modern web interfaces with React.js',
                'short_description_ar': 'بناء واجهات ويب حديثة باستخدام React.js',
                'price': 79.99,
                'difficulty_level': 'beginner',
                'duration_weeks': 8,
                'requirements': 'JavaScript fundamentals\nHTML/CSS knowledge\nBasic programming concepts',
                'requirements_ar': 'أساسيات JavaScript\nمعرفة HTML/CSS\nمفاهيم البرمجة الأساسية',
                'what_you_learn': 'React components and JSX\nState management with hooks\nRouting and navigation\nAPI integration\nModern development tools',
                'what_you_learn_ar': 'مكونات React وJSX\nإدارة الحالة باستخدام hooks\nالتوجيه والتنقل\nتكامل API\nأدوات التطوير الحديثة',
                'is_featured': True
            },
            {
                'title': 'Python Data Science Masterclass',
                'title_ar': 'الدورة الشاملة لعلم البيانات باستخدام Python',
                'category': categories[1],  # Data Science
                'instructor': instructors[2],
                'description': 'Comprehensive data science course covering pandas, numpy, matplotlib, and machine learning with scikit-learn.',
                'description_ar': 'دورة شاملة في علم البيانات تغطي pandas وnumpy وmatplotlib والتعلم الآلي باستخدام scikit-learn.',
                'short_description': 'Master data analysis and machine learning with Python',
                'short_description_ar': 'إتقان تحليل البيانات والتعلم الآلي باستخدام Python',
                'price': 129.99,
                'difficulty_level': 'intermediate',
                'duration_weeks': 16,
                'requirements': 'Python programming basics\nStatistics fundamentals\nMathematics background',
                'requirements_ar': 'أساسيات برمجة Python\nأساسيات الإحصاء\nخلفية رياضية',
                'what_you_learn': 'Data manipulation with pandas\nData visualization\nMachine learning algorithms\nStatistical analysis\nReal-world projects',
                'what_you_learn_ar': 'معالجة البيانات باستخدام pandas\nتصور البيانات\nخوارزميات التعلم الآلي\nالتحليل الإحصائي\nمشاريع من العالم الحقيقي',
                'is_featured': False
            },
            {
                'title': 'Flutter Mobile App Development',
                'title_ar': 'تطوير تطبيقات الجوال باستخدام Flutter',
                'category': categories[2],  # Mobile Development
                'instructor': instructors[0],
                'description': 'Build beautiful cross-platform mobile apps with Flutter and Dart programming language.',
                'description_ar': 'بناء تطبيقات جوال جميلة ومتعددة المنصات باستخدام Flutter ولغة البرمجة Dart.',
                'short_description': 'Create cross-platform mobile apps with Flutter',
                'short_description_ar': 'إنشاء تطبيقات جوال متعددة المنصات باستخدام Flutter',
                'price': 89.99,
                'difficulty_level': 'beginner',
                'duration_weeks': 10,
                'requirements': 'Basic programming knowledge\nMobile development interest\nDart language basics',
                'requirements_ar': 'معرفة أساسية بالبرمجة\nاهتمام بتطوير الجوال\nأساسيات لغة Dart',
                'what_you_learn': 'Flutter widgets and layouts\nState management\nNavigation and routing\nAPI integration\nApp store deployment',
                'what_you_learn_ar': 'widgets وlayouts في Flutter\nإدارة الحالة\nالتنقل والتوجيه\nتكامل API\nنشر في متاجر التطبيقات',
                'is_featured': False
            },
            {
                'title': 'Docker and Kubernetes DevOps',
                'title_ar': 'Docker وKubernetes للديف أوبس',
                'category': categories[3],  # DevOps
                'instructor': instructors[1],
                'description': 'Learn containerization with Docker and orchestration with Kubernetes for modern DevOps practices.',
                'description_ar': 'تعلم الحاويات باستخدام Docker والتنسيق باستخدام Kubernetes لممارسات DevOps الحديثة.',
                'short_description': 'Master containerization and orchestration technologies',
                'short_description_ar': 'إتقان تقنيات الحاويات والتنسيق',
                'price': 149.99,
                'difficulty_level': 'advanced',
                'duration_weeks': 14,
                'requirements': 'Linux command line\nBasic networking\nServer administration\nCloud concepts',
                'requirements_ar': 'سطر أوامر Linux\nأساسيات الشبكات\nإدارة الخوادم\nمفاهيم الحوسبة السحابية',
                'what_you_learn': 'Docker containerization\nKubernetes orchestration\nCI/CD pipelines\nMonitoring and logging\nCloud deployment',
                'what_you_learn_ar': 'حاويات Docker\nتنسيق Kubernetes\nخطوط CI/CD\nالمراقبة والسجلات\nالنشر السحابي',
                'is_featured': True
            },
            {
                'title': 'JavaScript Fundamentals',
                'title_ar': 'أساسيات JavaScript',
                'category': categories[0],  # Web Development
                'instructor': instructors[2],
                'description': 'Learn JavaScript from scratch including ES6+ features, DOM manipulation, and asynchronous programming.',
                'description_ar': 'تعلم JavaScript من الصفر بما في ذلك ميزات ES6+ ومعالجة DOM والبرمجة غير المتزامنة.',
                'short_description': 'Complete JavaScript course for beginners',
                'short_description_ar': 'دورة JavaScript كاملة للمبتدئين',
                'price': 59.99,
                'difficulty_level': 'beginner',
                'duration_weeks': 6,
                'requirements': 'Basic HTML/CSS\nProgramming interest\nNo prior JavaScript experience needed',
                'requirements_ar': 'أساسيات HTML/CSS\nاهتمام بالبرمجة\nلا حاجة لخبرة سابقة في JavaScript',
                'what_you_learn': 'JavaScript syntax and concepts\nDOM manipulation\nEvent handling\nAsync/await programming\nModern ES6+ features',
                'what_you_learn_ar': 'بناء جملة ومفاهيم JavaScript\nمعالجة DOM\nتعامل مع الأحداث\nبرمجة Async/await\nميزات ES6+ الحديثة',
                'is_featured': False
            }
        ]

        courses = []
        for course_data in courses_data:
            course, created = Course.objects.get_or_create(
                title=course_data['title'],
                defaults=course_data
            )
            courses.append(course)

        # Create sections and lessons for each course
        for course in courses:
            # Create 3-5 sections per course
            num_sections = random.randint(3, 5)
            for i in range(num_sections):
                section, created = Section.objects.get_or_create(
                    course=course,
                    title=f"Section {i+1}: {['Introduction', 'Core Concepts', 'Advanced Topics', 'Practice Projects', 'Final Project'][i]}",
                    defaults={
                        'title_ar': f"القسم {i+1}: {['المقدمة', 'المفاهيم الأساسية', 'المواضيع المتقدمة', 'مشاريع التطبيق', 'المشروع النهائي'][i]}",
                        'description': f"This section covers {['basic introduction', 'fundamental concepts', 'advanced techniques', 'hands-on practice', 'capstone project'][i]}",
                        'description_ar': f"هذا القسم يغطي {['المقدمة الأساسية', 'المفاهيم الأساسية', 'التقنيات المتقدمة', 'التطبيق العملي', 'المشروع الختامي'][i]}",
                        'order': i + 1
                    }
                )

                # Create 3-7 lessons per section
                num_lessons = random.randint(3, 7)
                for j in range(num_lessons):
                    lesson_types = ['video', 'text', 'video', 'text', 'video']
                    lesson_type = lesson_types[j % len(lesson_types)]
                    
                    Lesson.objects.get_or_create(
                        section=section,
                        title=f"Lesson {j+1}: {['Getting Started', 'Basic Implementation', 'Advanced Features', 'Best Practices', 'Common Patterns', 'Troubleshooting', 'Summary'][j]}",
                        defaults={
                            'title_ar': f"الدرس {j+1}: {['البداية', 'التنفيذ الأساسي', 'الميزات المتقدمة', 'أفضل الممارسات', 'الأنماط الشائعة', 'حل المشاكل', 'الملخص'][j]}",
                            'description': f"Learn about {lesson_type} content in this comprehensive lesson.",
                            'description_ar': f"تعلم حول محتوى {lesson_type} في هذا الدرس الشامل.",
                            'lesson_type': lesson_type,
                            'duration_minutes': random.randint(10, 45),
                            'content': f"This is the content for {lesson_type} lesson. It includes detailed explanations and examples.",
                            'content_ar': f"هذا هو المحتوى لدرس {lesson_type}. يتضمن شروحات مفصلة وأمثلة.",
                            'order': j + 1,
                            'is_preview': j == 0,  # First lesson is preview
                        }
                    )

        # Create some student users
        students_data = [
            {'username': 'student1', 'first_name': 'Alice', 'last_name': 'Johnson', 'email': 'alice@student.com'},
            {'username': 'student2', 'first_name': 'Bob', 'last_name': 'Brown', 'email': 'bob@student.com'},
            {'username': 'student3', 'first_name': 'Carol', 'last_name': 'Davis', 'email': 'carol@student.com'},
        ]

        students = []
        for data in students_data:
            student, created = User.objects.get_or_create(
                username=data['username'],
                defaults={
                    'first_name': data['first_name'],
                    'last_name': data['last_name'],
                    'email': data['email']
                }
            )
            if created:
                student.set_password('student123')
                student.save()
            students.append(student)

        # Create some purchases
        for student in students:
            # Each student purchases 1-3 random courses
            purchased_courses = random.sample(courses, random.randint(1, 3))
            for course in purchased_courses:
                Purchase.objects.get_or_create(
                    user=student,
                    course=course,
                    defaults={
                        'amount_paid': course.price,
                        'is_completed': True
                    }
                )

        # Create some reviews
        review_texts = [
            "Excellent course! Very well structured and easy to follow.",
            "Great content and practical examples. Highly recommended!",
            "The instructor explains concepts clearly. Worth every penny.",
            "Good course but could use more hands-on exercises.",
            "Amazing depth of content. Perfect for intermediate learners.",
        ]

        for student in students:
            student_purchases = Purchase.objects.filter(user=student, is_completed=True)
            for purchase in student_purchases:
                if random.choice([True, False]):  # 50% chance of leaving a review
                    CourseReview.objects.get_or_create(
                        course=purchase.course,
                        user=student,
                        defaults={
                            'rating': random.randint(4, 5),
                            'review': random.choice(review_texts)
                        }
                    )

        self.stdout.write(self.style.SUCCESS('Successfully created sample data!'))
        self.stdout.write(f'Created:')
        self.stdout.write(f'- {Category.objects.count()} categories')
        self.stdout.write(f'- {Course.objects.count()} courses')
        self.stdout.write(f'- {Section.objects.count()} sections')
        self.stdout.write(f'- {Lesson.objects.count()} lessons')
        self.stdout.write(f'- {User.objects.count()} users')
        self.stdout.write(f'- {Purchase.objects.count()} purchases')
        self.stdout.write(f'- {CourseReview.objects.count()} reviews')
        
        self.stdout.write('\nLogin credentials:')
        self.stdout.write('Admin: admin / admin123')
        self.stdout.write('Instructors: john_doe, jane_smith, mike_wilson / instructor123')
        self.stdout.write('Students: student1, student2, student3 / student123')
