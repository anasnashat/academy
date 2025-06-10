from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from blog.models import Category, Tag, Post, Comment
from django.utils import timezone
import random
from datetime import timedelta


class Command(BaseCommand):
    help = 'Populate the blog with sample data'

    def handle(self, *args, **options):
        self.stdout.write('Starting blog data population...')
        
        # Create categories
        self.create_categories()
        
        # Create tags
        self.create_tags()
        
        # Create posts
        self.create_posts()
        
        # Create comments
        self.create_comments()
        
        self.stdout.write(self.style.SUCCESS('Blog data population completed successfully!'))

    def create_categories(self):
        """Create blog categories"""
        categories = [
            'Web Development',
            'Data Science',
            'Mobile Development',
            'DevOps',
            'Programming Languages',
            'Career Advice'
        ]
        
        for category_name in categories:
            category, created = Category.objects.get_or_create(name=category_name)
            if created:
                self.stdout.write(f'Created category: {category.name}')

    def create_tags(self):
        """Create blog tags"""
        tags_list = [
            'python', 'django', 'javascript', 'react', 'vue', 'angular', 'nodejs', 'express',
            'api', 'rest', 'graphql', 'database', 'postgresql', 'mysql', 'mongodb', 'redis',
            'docker', 'kubernetes', 'aws', 'azure', 'gcp', 'devops', 'cicd', 'testing',
            'unit-testing', 'integration-testing', 'frontend', 'backend', 'fullstack',
            'machine-learning', 'ai', 'data-science', 'pandas', 'numpy', 'tensorflow',
            'pytorch', 'scikit-learn', 'visualization', 'mobile', 'ios', 'android',
            'react-native', 'flutter', 'swift', 'kotlin', 'java', 'csharp', 'php', 'ruby',
            'git', 'github', 'gitlab', 'version-control', 'agile', 'scrum',
            'project-management', 'team-collaboration', 'code-review', 'security',
            'authentication', 'authorization', 'encryption', 'performance', 'optimization',
            'scalability', 'microservices', 'architecture', 'design-patterns', 'clean-code',
            'refactoring', 'debugging', 'troubleshooting'
        ]
        
        for tag_name in tags_list:
            tag, created = Tag.objects.get_or_create(name=tag_name)
            if created:
                self.stdout.write(f'Created tag: {tag.name}')

    def create_posts(self):
        """Create blog posts"""
        # Get all users, categories, and tags
        users = list(User.objects.all())
        categories = list(Category.objects.all())
        tags = list(Tag.objects.all())

        if not users:
            self.stdout.write(self.style.WARNING('No users found. Creating a default author...'))
            author = User.objects.create_user(
                username='blog_author',
                email='author@academy.com',
                first_name='Blog',
                last_name='Author'
            )
            users = [author]

        posts_data = [
            {
                'title': 'Getting Started with Django: A Comprehensive Guide',
                'featured_image': 'blog/django-guide.svg',
                'content': '''
Django is a high-level Python web framework that encourages rapid development and clean, pragmatic design. Built by experienced developers, it takes care of much of the hassle of web development, so you can focus on writing your app without needing to reinvent the wheel.

## Why Choose Django?

Django follows the "Don't Repeat Yourself" (DRY) principle. The framework is designed to help developers take applications from concept to completion as quickly as possible.

### Key Features:

1. **Admin Interface**: Django provides a built-in admin interface that's ready to use out of the box.
2. **ORM**: Object-Relational Mapping that allows you to interact with your database using Python code.
3. **Security**: Django takes security seriously and helps developers avoid many common security mistakes.
4. **Scalability**: Django is used by many high-traffic sites and can scale to meet heavy demands.

## Getting Started

To start a new Django project:

```bash
pip install django
django-admin startproject myproject
cd myproject
python manage.py runserver
```

## Models and Database

Django's ORM allows you to define your data models as Python classes:

```python
from django.db import models

class Post(models.Model):
    title = models.CharField(max_length=200)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return self.title
```

## Views and URLs

Django views handle the logic for your web pages:

```python
from django.shortcuts import render
from .models import Post

def post_list(request):
    posts = Post.objects.all()
    return render(request, 'blog/post_list.html', {'posts': posts})
```

Django makes it easy to build powerful web applications quickly and efficiently.
                ''',
                'reading_time': 8,
                'featured': True,
                'tags': ['django', 'python', 'web', 'backend', 'framework']
            },
            {
                'title': 'Modern JavaScript ES6+ Features Every Developer Should Know',
                'featured_image': 'blog/javascript-es6.svg',
                'content': '''
JavaScript has evolved significantly over the years. ES6 (ECMAScript 2015) and subsequent versions have introduced many powerful features that make JavaScript more expressive and easier to work with.

## Arrow Functions

Arrow functions provide a concise syntax for writing functions:

```javascript
// Traditional function
function add(a, b) {
    return a + b;
}

// Arrow function
const add = (a, b) => a + b;
```

## Destructuring

Destructuring allows you to extract values from arrays or objects:

```javascript
// Array destructuring
const [first, second] = [1, 2, 3];

// Object destructuring
const {name, age} = {name: 'John', age: 30, city: 'New York'};
```

## Template Literals

Template literals make string interpolation much easier:

```javascript
const name = 'World';
const greeting = `Hello, ${name}!`;
```

## Async/Await

Async/await makes working with promises much cleaner:

```javascript
async function fetchData() {
    try {
        const response = await fetch('/api/data');
        const data = await response.json();
        return data;
    } catch (error) {
        console.error('Error:', error);
    }
}
```

## Modules

ES6 modules allow you to organize your code better:

```javascript
// math.js
export const add = (a, b) => a + b;
export const subtract = (a, b) => a - b;

// main.js
import { add, subtract } from './math.js';
```

These modern JavaScript features help you write cleaner, more maintainable code.
                ''',
                'reading_time': 6,
                'featured': True,
                'tags': ['javascript', 'es6', 'frontend', 'web']
            },
            {
                'title': 'Building RESTful APIs with Django REST Framework',
                'content': '''
Django REST Framework (DRF) is a powerful toolkit for building Web APIs in Django. It provides a flexible and customizable framework that makes it easy to build and test APIs.

## Why Use DRF?

1. **Serialization**: Easy conversion between Django models and JSON/XML
2. **Authentication**: Multiple authentication methods out of the box
3. **Permissions**: Fine-grained permission control
4. **Browsable API**: Interactive API documentation
5. **Testing**: Comprehensive testing tools

## Installation

```bash
pip install djangorestframework
```

Add it to your INSTALLED_APPS:

```python
INSTALLED_APPS = [
    # ...
    'rest_framework',
]
```

## Creating Serializers

```python
from rest_framework import serializers
from .models import Post

class PostSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = '__all__'
```

## Creating Views

```python
from rest_framework import generics
from .models import Post
from .serializers import PostSerializer

class PostListCreateView(generics.ListCreateAPIView):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
```

## URL Configuration

```python
from django.urls import path
from . import views

urlpatterns = [
    path('api/posts/', views.PostListCreateView.as_view()),
]
```

DRF makes building robust APIs straightforward and enjoyable.
                ''',
                'reading_time': 10,
                'featured': False,
                'tags': ['django', 'api', 'rest', 'python', 'backend']
            },
            {
                'title': 'Introduction to Machine Learning with Python',
                'content': '''
Machine Learning (ML) is a subset of artificial intelligence that enables computers to learn and make decisions from data without being explicitly programmed.

## What is Machine Learning?

Machine Learning algorithms build mathematical models based on training data to make predictions or decisions without being explicitly programmed to perform the task.

## Types of Machine Learning

### 1. Supervised Learning
- Uses labeled training data
- Examples: Classification, Regression
- Algorithms: Linear Regression, Decision Trees, Random Forest

### 2. Unsupervised Learning
- Uses unlabeled data
- Examples: Clustering, Dimensionality Reduction
- Algorithms: K-Means, PCA, DBSCAN

### 3. Reinforcement Learning
- Learns through interaction with environment
- Examples: Game playing, Robotics
- Algorithms: Q-Learning, Policy Gradient

## Getting Started with Python

Python is the most popular language for ML due to its rich ecosystem:

```python
import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression

# Load data
data = pd.read_csv('data.csv')

# Prepare features and target
X = data.drop('target', axis=1)
y = data['target']

# Split data
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2)

# Train model
model = LinearRegression()
model.fit(X_train, y_train)

# Make predictions
predictions = model.predict(X_test)
```

## Essential Libraries

- **NumPy**: Numerical computing
- **Pandas**: Data manipulation
- **Scikit-learn**: Machine learning algorithms
- **Matplotlib/Seaborn**: Data visualization
- **TensorFlow/PyTorch**: Deep learning

## ML Workflow

1. **Data Collection**: Gather relevant data
2. **Data Preprocessing**: Clean and prepare data
3. **Feature Engineering**: Select and create features
4. **Model Selection**: Choose appropriate algorithm
5. **Training**: Fit the model to training data
6. **Evaluation**: Test model performance
7. **Deployment**: Make the model available for use

This field is rapidly evolving, and there's always something new to learn!
                ''',
                'reading_time': 12,
                'featured': True,
                'tags': ['machine-learning', 'python', 'data-science', 'ai', 'scikit-learn', 'pandas', 'numpy']
            },
            {
                'title': 'Docker Containerization: From Development to Production',
                'featured_image': 'blog/docker-guide.svg',
                'content': '''
Docker has revolutionized how we develop, ship, and run applications. Containerization solves the "it works on my machine" problem by packaging applications with all their dependencies.

## What is Docker?

Docker is a platform that uses containerization technology to package applications and their dependencies into lightweight, portable containers.

## Key Concepts

### Images
Templates for creating containers. Think of them as blueprints.

### Containers
Running instances of images. They're isolated and include everything needed to run the application.

### Dockerfile
A text file with instructions for building Docker images:

```dockerfile
FROM python:3.9
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .
EXPOSE 8000
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
```

## Basic Commands

```bash
# Build an image
docker build -t myapp .

# Run a container
docker run -p 8000:8000 myapp

# List running containers
docker ps

# Stop a container
docker stop container_id
```

## Docker Compose

For multi-container applications:

```yaml
version: '3.8'
services:
  web:
    build: .
    ports:
      - "8000:8000"
    depends_on:
      - db
  db:
    image: postgres:13
    environment:
      POSTGRES_DB: myapp
      POSTGRES_USER: user
      POSTGRES_PASSWORD: password
```

## Benefits

1. **Consistency**: Same environment everywhere
2. **Isolation**: Applications don't interfere with each other
3. **Portability**: Run anywhere Docker is installed
4. **Scalability**: Easy to scale up or down
5. **Resource Efficiency**: Lighter than virtual machines

## Best Practices

- Use official base images
- Minimize image layers
- Use .dockerignore file
- Don't run as root user
- Use multi-stage builds for smaller images

Docker transforms how we think about application deployment and makes DevOps practices more accessible.
                ''',
                'reading_time': 9,
                'featured': False,
                'tags': ['docker', 'containerization', 'devops', 'deployment', 'infrastructure']
            },
            {
                'title': 'React Hooks: A Complete Guide to Modern React Development',
                'featured_image': 'blog/react-hooks.svg',
                'content': '''
React Hooks have fundamentally changed how we write React components. They allow you to use state and other React features in functional components, making code more readable and reusable.

## What are React Hooks?

Hooks are functions that let you "hook into" React state and lifecycle features from functional components. They start with the word "use".

## Built-in Hooks

### useState
Manages component state:

```jsx
import React, { useState } from 'react';

function Counter() {
    const [count, setCount] = useState(0);
    
    return (
        <div>
            <p>Count: {count}</p>
            <button onClick={() => setCount(count + 1)}>
                Increment
            </button>
        </div>
    );
}
```

### useEffect
Handles side effects and lifecycle methods:

```jsx
import React, { useState, useEffect } from 'react';

function UserProfile({ userId }) {
    const [user, setUser] = useState(null);
    
    useEffect(() => {
        fetch(`/api/users/${userId}`)
            .then(response => response.json())
            .then(userData => setUser(userData));
    }, [userId]); // Dependency array
    
    return <div>{user ? user.name : 'Loading...'}</div>;
}
```

### useContext
Consumes React context:

```jsx
import React, { useContext } from 'react';
import { ThemeContext } from './ThemeContext';

function ThemedButton() {
    const theme = useContext(ThemeContext);
    
    return (
        <button style={{ backgroundColor: theme.primary }}>
            Themed Button
        </button>
    );
}
```

## Custom Hooks

Create reusable stateful logic:

```jsx
function useLocalStorage(key, initialValue) {
    const [storedValue, setStoredValue] = useState(() => {
        try {
            const item = window.localStorage.getItem(key);
            return item ? JSON.parse(item) : initialValue;
        } catch (error) {
            return initialValue;
        }
    });
    
    const setValue = (value) => {
        try {
            setStoredValue(value);
            window.localStorage.setItem(key, JSON.stringify(value));
        } catch (error) {
            console.error(error);
        }
    };
    
    return [storedValue, setValue];
}
```

## Rules of Hooks

1. Only call hooks at the top level
2. Only call hooks from React functions
3. Use the ESLint plugin for React Hooks

## Benefits

- **Reusability**: Logic can be shared between components
- **Simplicity**: No need for class components
- **Testing**: Easier to test individual pieces of logic
- **Performance**: Built-in optimization with useMemo and useCallback

React Hooks represent the future of React development, making functional components more powerful than ever.
                ''',
                'reading_time': 11,
                'featured': True,
                'tags': ['react', 'hooks', 'javascript', 'frontend', 'web', 'components']
            },
            {
                'title': 'Database Design Best Practices for Web Applications',
                'content': '''
Good database design is crucial for building scalable and maintainable web applications. Poor design decisions early on can lead to performance issues and technical debt that's expensive to fix later.

## Database Design Principles

### 1. Normalization
Organize data to reduce redundancy and improve data integrity:

```sql
-- Normalized structure
CREATE TABLE users (
    id SERIAL PRIMARY KEY,
    username VARCHAR(50) UNIQUE,
    email VARCHAR(100) UNIQUE
);

CREATE TABLE posts (
    id SERIAL PRIMARY KEY,
    title VARCHAR(200),
    content TEXT,
    author_id INTEGER REFERENCES users(id),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

### 2. Use Appropriate Data Types
Choose the most efficient data type for each column:

```sql
-- Good
user_id INTEGER
price DECIMAL(10,2)
is_active BOOLEAN
created_at TIMESTAMP

-- Avoid
user_id VARCHAR(50)  -- when you need integer
price VARCHAR(20)    -- for monetary values
is_active VARCHAR(10) -- for true/false values
```

### 3. Indexing Strategy
Create indexes for frequently queried columns:

```sql
-- Primary key (automatically indexed)
CREATE TABLE products (
    id SERIAL PRIMARY KEY,
    name VARCHAR(200),
    category_id INTEGER,
    price DECIMAL(10,2),
    created_at TIMESTAMP
);

-- Indexes for common queries
CREATE INDEX idx_products_category ON products(category_id);
CREATE INDEX idx_products_price ON products(price);
CREATE INDEX idx_products_created ON products(created_at);
```

## Relationships

### One-to-Many
Most common relationship type:

```sql
CREATE TABLE categories (
    id SERIAL PRIMARY KEY,
    name VARCHAR(100)
);

CREATE TABLE products (
    id SERIAL PRIMARY KEY,
    name VARCHAR(200),
    category_id INTEGER REFERENCES categories(id)
);
```

### Many-to-Many
Use junction tables:

```sql
CREATE TABLE users (
    id SERIAL PRIMARY KEY,
    username VARCHAR(50)
);

CREATE TABLE roles (
    id SERIAL PRIMARY KEY,
    name VARCHAR(50)
);

CREATE TABLE user_roles (
    user_id INTEGER REFERENCES users(id),
    role_id INTEGER REFERENCES roles(id),
    PRIMARY KEY (user_id, role_id)
);
```

## Performance Considerations

### Query Optimization
- Use EXPLAIN to analyze query performance
- Avoid SELECT * in production code
- Use appropriate WHERE clauses
- Consider query caching

### Database Connection Pooling
```python
# Django example
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'mydb',
        'CONN_MAX_AGE': 600,  # Connection pooling
    }
}
```

## Security Best Practices

1. **Use parameterized queries** to prevent SQL injection
2. **Implement proper authentication** and authorization
3. **Encrypt sensitive data** at rest and in transit
4. **Regular backups** and disaster recovery plans
5. **Monitor database access** and audit logs

## Scaling Strategies

- **Read replicas** for read-heavy workloads
- **Sharding** for horizontal scaling
- **Caching layers** (Redis, Memcached)
- **Database partitioning** for large tables

Good database design is an investment that pays dividends throughout the life of your application.
                ''',
                'reading_time': 13,
                'featured': False,
                'tags': ['database', 'sql', 'postgresql', 'mysql', 'performance', 'scaling', 'design']
            },
            {
                'title': 'Career Tips for Software Developers in 2024',
                'content': '''
The software development landscape continues to evolve rapidly. Here are essential career tips to help you thrive as a developer in 2024 and beyond.

## Technical Skills to Focus On

### Core Programming Fundamentals
Master the fundamentals that never go out of style:
- Data structures and algorithms
- Object-oriented programming
- Functional programming concepts
- System design principles

### In-Demand Technologies
Stay current with trending technologies:
- **Cloud Platforms**: AWS, Azure, Google Cloud
- **Containerization**: Docker, Kubernetes
- **AI/ML**: Python, TensorFlow, PyTorch
- **Modern Frameworks**: React, Vue, Angular, Next.js
- **Backend**: Node.js, Python, Go, Rust

## Soft Skills Matter

### Communication
- Write clear documentation
- Explain technical concepts to non-technical stakeholders
- Participate actively in code reviews
- Ask good questions

### Collaboration
- Work effectively in cross-functional teams
- Understand business requirements
- Practice empathy with users and colleagues
- Embrace remote work best practices

## Continuous Learning Strategy

### Stay Updated
```
// Your learning routine might look like:
Weekly: Read tech blogs, follow industry leaders
Monthly: Try a new tool or framework
Quarterly: Complete an online course or certification
Annually: Attend conferences or workshops
```

### Build Projects
- Create side projects that showcase your skills
- Contribute to open source projects
- Document your learning journey
- Build a portfolio that tells your story

## Career Growth Paths

### Individual Contributor Track
- Junior Developer → Senior Developer → Staff Engineer → Principal Engineer

### Management Track
- Senior Developer → Team Lead → Engineering Manager → Director

### Specialist Tracks
- Security Engineer
- DevOps Engineer
- Data Engineer
- Machine Learning Engineer

## Building Your Professional Network

### Online Presence
- Maintain an updated LinkedIn profile
- Share knowledge through blog posts
- Participate in tech communities
- Showcase projects on GitHub

### Offline Networking
- Attend local meetups and conferences
- Join professional organizations
- Find a mentor in your field
- Mentor others when you can

## Job Search Tips

### Preparation
- Practice coding interviews regularly
- Prepare system design scenarios
- Research the company and role thoroughly
- Prepare thoughtful questions for interviewers

### Interview Success
- Communicate your thought process clearly
- Show enthusiasm for learning
- Demonstrate problem-solving skills
- Be honest about what you don't know

## Work-Life Balance

### Avoid Burnout
- Set boundaries between work and personal time
- Take regular breaks and vacations
- Pursue hobbies outside of coding
- Maintain physical and mental health

### Remote Work Success
- Create a dedicated workspace
- Establish routine and boundaries
- Overcommunicate with your team
- Invest in good equipment and internet

## Negotiating Your Worth

### Know Your Value
- Research market salaries for your role and location
- Document your achievements and impact
- Understand the total compensation package
- Consider non-monetary benefits

The key to a successful developer career is continuous learning, building strong relationships, and staying adaptable to change.
                ''',
                'reading_time': 15,
                'featured': True,
                'tags': ['career', 'professional-development', 'skills', 'networking', 'growth']
            }
        ]

        for post_data in posts_data:
            # Get random category
            category = random.choice(categories)
            
            # Get random author
            author = random.choice(users)
            
            # Create post
            post = Post.objects.create(
                title=post_data['title'],
                content=post_data['content'],
                author=author,
                category=category,
                reading_time=post_data['reading_time'],
                featured=post_data['featured'],
                featured_image=post_data.get('featured_image', ''),
                published_at=timezone.now() - timedelta(days=random.randint(1, 30))
            )
            
            # Add tags
            post_tags = [tag for tag in tags if tag.name in post_data['tags']]
            post.tags.set(random.sample(post_tags, min(len(post_tags), random.randint(3, 6))))
            
            # Update view count
            post.views = random.randint(50, 500)
            post.save()
            
            self.stdout.write(f'Created post: {post.title}')

    def create_comments(self):
        """Create sample comments"""
        posts = list(Post.objects.all())
        users = list(User.objects.all())
        
        if not users:
            return
        
        # Sample comment texts
        comment_texts = [
            "Great article! This really helped me understand the concepts better.",
            "Thanks for sharing this. I've been looking for exactly this information.",
            "Excellent explanation. Could you also cover advanced topics in a future post?",
            "I tried this approach and it worked perfectly. Thank you!",
            "Very well written and easy to follow. Looking forward to more content like this.",
            "This is exactly what I needed for my current project. Much appreciated!",
            "Clear and concise explanation. The code examples are particularly helpful.",
            "Awesome post! I've bookmarked this for future reference.",
            "Really insightful content. I learned something new today.",
            "Perfect timing! I was just struggling with this exact problem.",
            "Love the practical examples. Makes it much easier to understand.",
            "This helped me solve a bug I've been working on for days. Thank you!",
            "Great tutorial! Step-by-step instructions are very clear.",
            "Fantastic resource. I'll definitely be sharing this with my team.",
            "Well-researched article with good examples. Keep up the great work!"
        ]
        
        reply_texts = [
            "Glad it was helpful!",
            "Thanks for the feedback!",
            "You're welcome! More content coming soon.",
            "Happy to help!",
            "Thanks for reading and commenting!",
            "Great to hear it worked for you!",
            "Appreciate the kind words!",
            "Thanks for sharing with your team!"
        ]
        
        # Create comments for each post
        for post in posts:
            num_comments = random.randint(3, 8)
            post_comments = []
            
            for _ in range(num_comments):
                comment = Comment.objects.create(
                    post=post,
                    author=random.choice(users),
                    content=random.choice(comment_texts),
                    created_at=timezone.now() - timedelta(
                        days=random.randint(0, 20),
                        hours=random.randint(0, 23),
                        minutes=random.randint(0, 59)
                    )
                )
                post_comments.append(comment)
                self.stdout.write(f'Created comment on post: {post.title}')
            
            # Create some replies to comments
            if post_comments:
                num_replies = random.randint(1, 3)
                for _ in range(num_replies):
                    parent_comment = random.choice(post_comments)
                    reply = Comment.objects.create(
                        post=post,
                        author=random.choice(users),
                        content=random.choice(reply_texts),
                        parent=parent_comment,
                        created_at=parent_comment.created_at + timedelta(
                            hours=random.randint(1, 48),
                            minutes=random.randint(0, 59)
                        )
                    )
                    self.stdout.write(f'Created reply to comment on: {post.title}')
