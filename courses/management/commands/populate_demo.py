"""
Management command to populate the database with demo courses, modules, and lessons.
Covers all categories and levels for a rich demo experience.
"""

from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from courses.models import Course, Module, Lesson

User = get_user_model()


DEMO_COURSES = [
    # ========== PROGRAMMING ==========
    {
        'title': 'Python Mastery: From Zero to Hero',
        'description': 'A comprehensive Python course covering everything from basics to advanced topics like decorators, generators, and OOP. Build real-world projects including a web scraper, automation scripts, and a CLI application. Perfect for beginners who want to become proficient Python developers.',
        'category': 'programming',
        'level': 'beginner',
        'price': 0,
        'modules': [
            {
                'title': 'Getting Started with Python',
                'lessons': [
                    {'title': 'Installing Python & Setting Up VS Code', 'content': 'Learn how to download and install Python on your system. We will also set up Visual Studio Code with the Python extension for a smooth development experience.\n\nStep 1: Visit python.org and download the latest version.\nStep 2: Run the installer and make sure to check "Add Python to PATH".\nStep 3: Install VS Code and add the Python extension.\nStep 4: Verify the installation by running python --version in your terminal.', 'duration_minutes': 15},
                    {'title': 'Your First Python Program', 'content': 'Write your very first Python program! We will explore the print() function, comments, and basic syntax.\n\n# Hello World\nprint("Hello, World!")\n\n# Variables\nname = "EduVerse"\nprint(f"Welcome to {name}!")\n\nPython uses indentation instead of braces, making code clean and readable.', 'duration_minutes': 20},
                    {'title': 'Variables and Data Types', 'content': 'Understand Python data types including integers, floats, strings, booleans, and None. Learn how to create variables and perform type conversion.\n\nPython is dynamically typed, meaning you don\'t need to declare variable types explicitly.', 'duration_minutes': 25},
                ]
            },
            {
                'title': 'Control Flow & Functions',
                'lessons': [
                    {'title': 'If/Else Statements & Loops', 'content': 'Master conditional logic with if, elif, and else statements. Learn for loops and while loops to iterate over data structures.', 'duration_minutes': 30},
                    {'title': 'Functions & Parameters', 'content': 'Learn to write reusable code with functions. Understand parameters, return values, default arguments, and *args/**kwargs.', 'duration_minutes': 25},
                    {'title': 'List Comprehensions & Lambda', 'content': 'Write Pythonic code with list comprehensions. Understand lambda functions and when to use them.', 'duration_minutes': 20},
                ]
            },
            {
                'title': 'Object-Oriented Programming',
                'lessons': [
                    {'title': 'Classes and Objects', 'content': 'Understand the fundamentals of OOP in Python. Create classes, instantiate objects, and use the __init__ constructor.', 'duration_minutes': 35},
                    {'title': 'Inheritance & Polymorphism', 'content': 'Learn how to extend classes using inheritance. Understand method overriding and polymorphism.', 'duration_minutes': 30},
                    {'title': 'Decorators & Generators', 'content': 'Advanced Python concepts: decorators for modifying function behavior and generators for memory-efficient iteration.', 'duration_minutes': 30},
                ]
            },
        ]
    },
    {
        'title': 'Advanced Java Programming',
        'description': 'Deep dive into Java with advanced topics including multithreading, collections framework, streams API, design patterns, and Spring Boot fundamentals. This course is designed for developers who already know Java basics and want to level up their skills.',
        'category': 'programming',
        'level': 'advanced',
        'price': 1499,
        'modules': [
            {
                'title': 'Advanced Collections & Generics',
                'lessons': [
                    {'title': 'Generics Deep Dive', 'content': 'Master Java generics including bounded types, wildcards, and type erasure.', 'duration_minutes': 40},
                    {'title': 'Collections Framework Internals', 'content': 'Understand how HashMap, TreeMap, LinkedList, and PriorityQueue work internally.', 'duration_minutes': 45},
                ]
            },
            {
                'title': 'Concurrency & Multithreading',
                'lessons': [
                    {'title': 'Threads, Executors & Thread Pools', 'content': 'Learn thread creation, executor service, and managing thread pools for concurrent applications.', 'duration_minutes': 50},
                    {'title': 'Synchronization & Locks', 'content': 'Understand race conditions, synchronized blocks, ReentrantLock, and concurrent collections.', 'duration_minutes': 45},
                ]
            },
            {
                'title': 'Design Patterns in Java',
                'lessons': [
                    {'title': 'Creational Patterns', 'content': 'Singleton, Factory, Builder, and Prototype patterns with real-world examples.', 'duration_minutes': 40},
                    {'title': 'Structural & Behavioral Patterns', 'content': 'Adapter, Observer, Strategy, and Command patterns implemented in Java.', 'duration_minutes': 40},
                ]
            },
        ]
    },

    # ========== WEB DEVELOPMENT ==========
    {
        'title': 'Full-Stack Web Development with Django',
        'description': 'Build production-ready web applications with Django! This course covers models, views, templates, forms, authentication, REST APIs, deployment, and best practices. You will build a complete e-commerce application from scratch.',
        'category': 'web_development',
        'level': 'intermediate',
        'price': 999,
        'modules': [
            {
                'title': 'Django Fundamentals',
                'lessons': [
                    {'title': 'Project Setup & MVT Architecture', 'content': 'Understand Django\'s Model-View-Template architecture. Set up a new project and create your first app.', 'duration_minutes': 30},
                    {'title': 'Models & Database Migrations', 'content': 'Define models, create migrations, use the Django ORM to query data efficiently.', 'duration_minutes': 35},
                    {'title': 'Views, URLs & Templates', 'content': 'Create function-based and class-based views. Configure URL routing and render dynamic templates.', 'duration_minutes': 35},
                ]
            },
            {
                'title': 'Authentication & Forms',
                'lessons': [
                    {'title': 'User Authentication System', 'content': 'Implement login, registration, logout, and password reset using Django\'s auth framework.', 'duration_minutes': 40},
                    {'title': 'Django Forms & Validation', 'content': 'Build forms with ModelForm, add custom validation, handle file uploads.', 'duration_minutes': 30},
                ]
            },
            {
                'title': 'REST API & Deployment',
                'lessons': [
                    {'title': 'Building REST APIs with DRF', 'content': 'Introduction to Django REST Framework. Create serializers, viewsets, and API endpoints.', 'duration_minutes': 45},
                    {'title': 'Deploying to Production', 'content': 'Deploy your Django app to a cloud server. Configure Gunicorn, Nginx, and PostgreSQL.', 'duration_minutes': 40},
                ]
            },
        ]
    },
    {
        'title': 'Modern React.js — Build Dynamic UIs',
        'description': 'Learn React.js from the ground up. Master components, hooks, state management with Redux, routing with React Router, and build a full-featured social media dashboard. Includes React 18 features and best practices.',
        'category': 'web_development',
        'level': 'beginner',
        'price': 799,
        'modules': [
            {
                'title': 'React Fundamentals',
                'lessons': [
                    {'title': 'JSX & Components', 'content': 'Understand JSX syntax and build your first React components. Learn about props and component composition.', 'duration_minutes': 25},
                    {'title': 'State & Event Handling', 'content': 'Manage component state with useState. Handle user events like clicks, input changes, and form submissions.', 'duration_minutes': 30},
                    {'title': 'useEffect & API Calls', 'content': 'Fetch data from APIs using useEffect. Understand the component lifecycle and cleanup functions.', 'duration_minutes': 35},
                ]
            },
            {
                'title': 'Advanced React Patterns',
                'lessons': [
                    {'title': 'Context API & Custom Hooks', 'content': 'Share state across components with Context. Build reusable custom hooks for common logic.', 'duration_minutes': 30},
                    {'title': 'React Router & Navigation', 'content': 'Implement client-side routing with React Router v6. Protected routes and dynamic parameters.', 'duration_minutes': 25},
                ]
            },
        ]
    },

    # ========== DATA SCIENCE ==========
    {
        'title': 'Data Science with Python & Pandas',
        'description': 'Master data analysis and visualization using Python. Learn NumPy, Pandas, Matplotlib, and Seaborn. Work with real datasets to extract insights and create compelling visualizations. Includes a capstone project analyzing a real-world dataset.',
        'category': 'data_science',
        'level': 'intermediate',
        'price': 1299,
        'modules': [
            {
                'title': 'NumPy & Data Manipulation',
                'lessons': [
                    {'title': 'NumPy Arrays & Operations', 'content': 'Create and manipulate NumPy arrays. Understand broadcasting, vectorization, and linear algebra operations.', 'duration_minutes': 35},
                    {'title': 'Pandas DataFrames', 'content': 'Load, explore, and manipulate data with Pandas. Filtering, grouping, merging, and pivot tables.', 'duration_minutes': 40},
                ]
            },
            {
                'title': 'Data Visualization',
                'lessons': [
                    {'title': 'Matplotlib & Seaborn Charts', 'content': 'Create line plots, bar charts, histograms, scatter plots, and heatmaps. Customize styles and annotations.', 'duration_minutes': 35},
                    {'title': 'Interactive Dashboards with Plotly', 'content': 'Build interactive visualizations and dashboards using Plotly Express.', 'duration_minutes': 30},
                ]
            },
            {
                'title': 'Capstone: Real-World Analysis',
                'lessons': [
                    {'title': 'Exploratory Data Analysis (EDA)', 'content': 'Analyze a real-world dataset end-to-end. Handle missing data, detect outliers, and find patterns.', 'duration_minutes': 50},
                    {'title': 'Presenting Data Insights', 'content': 'Create a professional data analysis report with key findings and actionable recommendations.', 'duration_minutes': 30},
                ]
            },
        ]
    },
    {
        'title': 'Machine Learning A-Z',
        'description': 'Comprehensive machine learning course covering supervised and unsupervised learning, neural networks basics, model evaluation, and deployment. Build predictive models using scikit-learn and real-world datasets.',
        'category': 'data_science',
        'level': 'advanced',
        'price': 1999,
        'modules': [
            {
                'title': 'Supervised Learning',
                'lessons': [
                    {'title': 'Linear & Logistic Regression', 'content': 'Understand regression for prediction. Implement linear regression, logistic regression, and evaluate with metrics.', 'duration_minutes': 45},
                    {'title': 'Decision Trees & Random Forests', 'content': 'Build tree-based models. Understand ensemble methods and hyperparameter tuning.', 'duration_minutes': 40},
                    {'title': 'Support Vector Machines', 'content': 'Learn SVM for classification problems. Understand kernel trick and margin maximization.', 'duration_minutes': 35},
                ]
            },
            {
                'title': 'Unsupervised Learning & Deployment',
                'lessons': [
                    {'title': 'Clustering with K-Means', 'content': 'Group similar data points using K-Means and hierarchical clustering. Determine optimal cluster count.', 'duration_minutes': 35},
                    {'title': 'Model Deployment with Flask', 'content': 'Deploy your trained ML model as a REST API using Flask. Create a prediction endpoint.', 'duration_minutes': 40},
                ]
            },
        ]
    },

    # ========== DESIGN ==========
    {
        'title': 'UI/UX Design Fundamentals',
        'description': 'Learn the principles of great user interface and user experience design. Master color theory, typography, layout systems, wireframing, and prototyping with Figma. Design a complete mobile app from concept to high-fidelity prototype.',
        'category': 'design',
        'level': 'beginner',
        'price': 599,
        'modules': [
            {
                'title': 'Design Principles',
                'lessons': [
                    {'title': 'Color Theory & Typography', 'content': 'Understand color harmonies, contrast ratios, and accessibility. Choose fonts that communicate your brand.', 'duration_minutes': 30},
                    {'title': 'Layout Systems & Grid Design', 'content': 'Master grid-based layouts. Understand spacing, alignment, and visual hierarchy.', 'duration_minutes': 25},
                    {'title': 'User Research & Personas', 'content': 'Learn to conduct user interviews, create personas, and map user journeys for better design decisions.', 'duration_minutes': 30},
                ]
            },
            {
                'title': 'Figma Mastery',
                'lessons': [
                    {'title': 'Figma Interface & Components', 'content': 'Navigate Figma workspace. Create reusable components, auto-layout, and design systems.', 'duration_minutes': 35},
                    {'title': 'Prototyping & Handoff', 'content': 'Create interactive prototypes with animations. Export assets and specs for developers.', 'duration_minutes': 30},
                ]
            },
        ]
    },

    # ========== BUSINESS ==========
    {
        'title': 'Startup Business Fundamentals',
        'description': 'Everything you need to know to launch and grow a startup. Covers business model canvas, market research, financial planning, fundraising, pitch decks, and growth strategies. Real case studies from successful startups.',
        'category': 'business',
        'level': 'beginner',
        'price': 0,
        'modules': [
            {
                'title': 'Ideation & Validation',
                'lessons': [
                    {'title': 'Finding Your Business Idea', 'content': 'Techniques for generating innovative business ideas. Problem-solution fit and market gap analysis.', 'duration_minutes': 25},
                    {'title': 'Market Research & Validation', 'content': 'Validate your idea before building. Customer interviews, surveys, and MVP testing strategies.', 'duration_minutes': 30},
                    {'title': 'Business Model Canvas', 'content': 'Map your entire business on a single page. Define value proposition, customer segments, and revenue streams.', 'duration_minutes': 25},
                ]
            },
            {
                'title': 'Funding & Growth',
                'lessons': [
                    {'title': 'Financial Planning & Budgeting', 'content': 'Create financial projections, understand burn rate, and plan your runway.', 'duration_minutes': 30},
                    {'title': 'Pitch Deck & Fundraising', 'content': 'Build a compelling pitch deck. Understand VC funding rounds from seed to Series A.', 'duration_minutes': 35},
                ]
            },
        ]
    },

    # ========== MARKETING ==========
    {
        'title': 'Digital Marketing Masterclass',
        'description': 'Complete digital marketing course covering SEO, Google Ads, social media marketing, content marketing, email marketing, and analytics. Learn to create and execute marketing campaigns that drive real results.',
        'category': 'marketing',
        'level': 'intermediate',
        'price': 899,
        'modules': [
            {
                'title': 'SEO & Content Marketing',
                'lessons': [
                    {'title': 'Search Engine Optimization (SEO)', 'content': 'On-page SEO, keyword research, technical SEO, and link building strategies to rank higher on Google.', 'duration_minutes': 40},
                    {'title': 'Content Marketing Strategy', 'content': 'Create a content calendar. Write blog posts, create videos, and distribute content effectively.', 'duration_minutes': 30},
                ]
            },
            {
                'title': 'Paid Advertising & Social Media',
                'lessons': [
                    {'title': 'Google Ads & PPC Campaigns', 'content': 'Set up Google Ads campaigns. Understand bidding strategies, ad copy, and conversion tracking.', 'duration_minutes': 35},
                    {'title': 'Social Media Marketing', 'content': 'Build brand presence on Instagram, LinkedIn, and Twitter. Organic and paid strategies.', 'duration_minutes': 30},
                    {'title': 'Email Marketing & Automation', 'content': 'Build email lists, design newsletters, set up drip campaigns, and analyze open/click rates.', 'duration_minutes': 25},
                ]
            },
        ]
    },

    # ========== PHOTOGRAPHY ==========
    {
        'title': 'Photography: Capture Stunning Images',
        'description': 'Learn photography from beginner to professional level. Master camera settings, composition rules, lighting techniques, portrait photography, landscape photography, and post-processing with Lightroom and Photoshop.',
        'category': 'photography',
        'level': 'beginner',
        'price': 699,
        'modules': [
            {
                'title': 'Camera Basics & Composition',
                'lessons': [
                    {'title': 'Understanding Your Camera', 'content': 'Learn about aperture, shutter speed, ISO, and how they work together in the exposure triangle.', 'duration_minutes': 25},
                    {'title': 'Composition Rules', 'content': 'Rule of thirds, leading lines, symmetry, framing, and negative space to create visually compelling images.', 'duration_minutes': 20},
                    {'title': 'Mastering Light', 'content': 'Natural light vs artificial light. Golden hour, blue hour, and how to use reflectors and diffusers.', 'duration_minutes': 30},
                ]
            },
            {
                'title': 'Post-Processing',
                'lessons': [
                    {'title': 'Lightroom Editing Workflow', 'content': 'Import, organize, and edit photos in Adobe Lightroom. Create presets for consistent styling.', 'duration_minutes': 35},
                    {'title': 'Advanced Photoshop Techniques', 'content': 'Retouching, compositing, and creative effects in Photoshop. Remove backgrounds and enhance portraits.', 'duration_minutes': 40},
                ]
            },
        ]
    },

    # ========== MUSIC ==========
    {
        'title': 'Music Production with Ableton Live',
        'description': 'Create professional music from your computer. Learn Ableton Live, sound design, mixing, mastering, and music theory. Produce complete tracks in genres like electronic, hip-hop, and pop. No prior music experience needed.',
        'category': 'music',
        'level': 'beginner',
        'price': 0,
        'modules': [
            {
                'title': 'Ableton Live Basics',
                'lessons': [
                    {'title': 'Interface & Session View', 'content': 'Navigate Ableton Live interface. Understand session view vs arrangement view, tracks, and clips.', 'duration_minutes': 20},
                    {'title': 'MIDI & Audio Recording', 'content': 'Record MIDI patterns with virtual instruments. Set up audio recording for vocals and guitars.', 'duration_minutes': 25},
                    {'title': 'Built-in Instruments & Effects', 'content': 'Explore Ableton synths like Wavetable and Operator. Use reverb, delay, and compression effects.', 'duration_minutes': 30},
                ]
            },
            {
                'title': 'Mixing & Mastering',
                'lessons': [
                    {'title': 'Mixing Fundamentals', 'content': 'Balance levels, pan instruments, use EQ and compression to create a polished mix.', 'duration_minutes': 35},
                    {'title': 'Mastering Your Track', 'content': 'Final polish: loudness maximization, stereo imaging, and preparing for distribution on Spotify/Apple Music.', 'duration_minutes': 30},
                ]
            },
        ]
    },

    # ========== MORE PROGRAMMING (INTERMEDIATE) ==========
    {
        'title': 'JavaScript ES6+ and Modern Development',
        'description': 'Master modern JavaScript features from ES6 to ES2024. Covers arrow functions, destructuring, promises, async/await, modules, classes, and more. Build practical projects to solidify your understanding.',
        'category': 'programming',
        'level': 'intermediate',
        'price': 599,
        'modules': [
            {
                'title': 'ES6+ Core Features',
                'lessons': [
                    {'title': 'Let, Const & Arrow Functions', 'content': 'Understand block scoping with let/const. Write concise functions with arrow syntax and implicit returns.', 'duration_minutes': 20},
                    {'title': 'Destructuring & Spread Operator', 'content': 'Extract values from arrays and objects elegantly. Use spread/rest operators for flexible function signatures.', 'duration_minutes': 25},
                    {'title': 'Template Literals & Enhanced Objects', 'content': 'Multi-line strings, string interpolation, computed property names, and shorthand methods.', 'duration_minutes': 20},
                ]
            },
            {
                'title': 'Async JavaScript',
                'lessons': [
                    {'title': 'Promises & Promise Chaining', 'content': 'Handle asynchronous operations with Promises. Understand resolve, reject, and chaining.', 'duration_minutes': 30},
                    {'title': 'Async/Await & Error Handling', 'content': 'Write clean async code with async/await. Proper error handling with try/catch.', 'duration_minutes': 25},
                    {'title': 'Fetch API & HTTP Requests', 'content': 'Make API calls with the Fetch API. Handle JSON responses and implement error handling.', 'duration_minutes': 25},
                ]
            },
        ]
    },
]


class Command(BaseCommand):
    help = 'Populate the database with demo courses, modules, and lessons'

    def handle(self, *args, **options):
        self.stdout.write(self.style.WARNING('Creating demo data...'))

        # Create instructor users
        instructors = []
        instructor_data = [
            {'username': 'prof_sharma', 'first_name': 'Ananya', 'last_name': 'Sharma', 'email': 'ananya@eduverse.com'},
            {'username': 'dr_patel', 'first_name': 'Rajesh', 'last_name': 'Patel', 'email': 'rajesh@eduverse.com'},
            {'username': 'tech_guru', 'first_name': 'Vikram', 'last_name': 'Mehta', 'email': 'vikram@eduverse.com'},
            {'username': 'creative_priya', 'first_name': 'Priya', 'last_name': 'Gupta', 'email': 'priya@eduverse.com'},
        ]

        for data in instructor_data:
            user, created = User.objects.get_or_create(
                username=data['username'],
                defaults={
                    'first_name': data['first_name'],
                    'last_name': data['last_name'],
                    'email': data['email'],
                    'role': 'instructor',
                }
            )
            if created:
                user.set_password('demo1234')
                user.save()
                self.stdout.write(f'  Created instructor: {user.get_full_name()}')
            instructors.append(user)

        # Create demo student
        student, created = User.objects.get_or_create(
            username='demo_student',
            defaults={
                'first_name': 'Demo',
                'last_name': 'Student',
                'email': 'student@eduverse.com',
                'role': 'student',
            }
        )
        if created:
            student.set_password('demo1234')
            student.save()
            self.stdout.write(f'  Created student: {student.get_full_name()}')

        # Create courses
        for i, course_data in enumerate(DEMO_COURSES):
            instructor = instructors[i % len(instructors)]
            modules_data = course_data.pop('modules')

            course, created = Course.objects.get_or_create(
                title=course_data['title'],
                defaults={
                    'description': course_data['description'],
                    'category': course_data['category'],
                    'level': course_data['level'],
                    'price': course_data['price'],
                    'instructor': instructor,
                    'is_published': True,
                }
            )

            if created:
                self.stdout.write(f'  Created course: {course.title} [{course.get_category_display()} / {course.get_level_display()}]')

                for m_order, module_data in enumerate(modules_data, start=1):
                    lessons_data = module_data.pop('lessons')
                    module = Module.objects.create(
                        course=course,
                        title=module_data['title'],
                        order=m_order,
                    )

                    for l_order, lesson_data in enumerate(lessons_data, start=1):
                        Lesson.objects.create(
                            module=module,
                            title=lesson_data['title'],
                            content=lesson_data['content'],
                            order=l_order,
                            duration_minutes=lesson_data.get('duration_minutes', 20),
                        )
            else:
                self.stdout.write(f'  Skipped (exists): {course.title}')

        total_courses = Course.objects.count()
        total_lessons = Lesson.objects.count()
        self.stdout.write(self.style.SUCCESS(
            f'\n✅ Done! {total_courses} courses with {total_lessons} total lessons across all categories & levels.'
        ))
        self.stdout.write(self.style.SUCCESS(
            '\nDemo Accounts:\n'
            '  Instructors: prof_sharma / dr_patel / tech_guru / creative_priya (password: demo1234)\n'
            '  Student: demo_student (password: demo1234)'
        ))
