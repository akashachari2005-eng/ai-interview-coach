"""
Skills Database
Contains all skills and keywords we look for in resumes
Author: Adarsh
"""

SKILLS_DB = [
    # Programming Languages
    'Python', 'Java', 'JavaScript', 'TypeScript', 'C++', 'C#', 'C',
    'Ruby', 'Go', 'Rust', 'Swift', 'Kotlin', 'PHP', 'R', 'Scala',
    'Perl', 'Dart', 'MATLAB', 'Assembly',

    # Web Frontend
    'React', 'React.js', 'Angular', 'Vue', 'Vue.js', 'Svelte',
    'HTML', 'HTML5', 'CSS', 'CSS3', 'SASS', 'LESS',
    'Tailwind', 'Tailwind CSS', 'Bootstrap', 'Material UI',
    'jQuery', 'Next.js', 'Nuxt.js', 'Redux', 'Webpack', 'Vite',

    # Web Backend
    'Node.js', 'Express', 'Express.js', 'Django', 'Flask', 'FastAPI',
    'Spring', 'Spring Boot', 'Laravel', 'Ruby on Rails',
    'ASP.NET', '.NET', 'Nest.js', 'Gin', 'Fiber',

    # Databases
    'SQL', 'MySQL', 'PostgreSQL', 'MongoDB', 'Redis', 'SQLite',
    'Oracle', 'Cassandra', 'DynamoDB', 'Firebase', 'Firestore',
    'MariaDB', 'CouchDB', 'Neo4j', 'Elasticsearch',

    # Cloud & DevOps
    'AWS', 'Amazon Web Services', 'Azure', 'Microsoft Azure',
    'GCP', 'Google Cloud', 'Google Cloud Platform',
    'Docker', 'Kubernetes', 'K8s', 'Jenkins', 'Travis CI',
    'CircleCI', 'GitHub Actions', 'Terraform', 'Ansible',
    'Nginx', 'Apache', 'Heroku', 'Vercel', 'Netlify',
    'DigitalOcean', 'Cloudflare',

    # Version Control
    'Git', 'GitHub', 'GitLab', 'Bitbucket', 'SVN',

    # Data Science & ML
    'Machine Learning', 'Deep Learning', 'Artificial Intelligence',
    'TensorFlow', 'PyTorch', 'Keras', 'Scikit-learn',
    'Pandas', 'NumPy', 'SciPy', 'Matplotlib', 'Seaborn',
    'OpenCV', 'NLP', 'Natural Language Processing',
    'Computer Vision', 'Data Analysis', 'Data Science',
    'Data Engineering', 'Big Data', 'Hadoop', 'Spark',
    'Apache Spark', 'Tableau', 'Power BI', 'Jupyter',

    # Mobile Development
    'Android', 'iOS', 'Flutter', 'React Native', 'Xamarin',
    'SwiftUI', 'Jetpack Compose', 'Ionic',

    # Testing
    'Selenium', 'JUnit', 'Jest', 'Mocha', 'Cypress',
    'Postman', 'pytest', 'Unit Testing', 'Integration Testing',

    # Others
    'Linux', 'Unix', 'Bash', 'Shell Scripting', 'PowerShell',
    'REST API', 'RESTful', 'GraphQL', 'WebSocket',
    'Microservices', 'Serverless', 'OAuth', 'JWT',
    'Agile', 'Scrum', 'JIRA', 'Trello', 'Figma',
    'CI/CD', 'DevOps', 'Blockchain', 'Solidity',
    'RabbitMQ', 'Kafka', 'Apache Kafka', 'gRPC',
]

EDUCATION_KEYWORDS = [
    'B.Tech', 'BTech', 'B.E.', 'BE',
    'M.Tech', 'MTech', 'M.E.', 'ME',
    'B.Sc', 'BSc', 'M.Sc', 'MSc',
    'B.C.A', 'BCA', 'M.C.A', 'MCA',
    'MBA', 'PhD', 'Ph.D',
    'Bachelor', 'Master', 'Diploma',
    'B.Com', 'BCom', 'M.Com', 'MCom',
    'B.A.', 'BA', 'M.A.', 'MA',
    'Computer Science', 'Information Technology',
    'Electrical Engineering', 'Mechanical Engineering',
    'Electronics', 'Civil Engineering',
]

QUESTION_TEMPLATES = {
    'technical_easy': [
        "What is {skill} and why is it used?",
        "Can you explain the basics of {skill}?",
        "What are the main features of {skill}?",
        "How did you first learn {skill}?",
        "What are the advantages of {skill}?",
    ],
    'technical_medium': [
        "Can you explain how you've used {skill} in your projects?",
        "What is the difference between {skill} and its alternatives?",
        "Describe a challenging problem you solved using {skill}.",
        "What are common mistakes developers make with {skill}?",
        "How do you handle errors and debugging in {skill}?",
        "What best practices do you follow when working with {skill}?",
        "Explain a key concept in {skill} that every developer should know.",
    ],
    'technical_hard': [
        "What's the most complex feature you've built with {skill}?",
        "How would you optimize performance in a {skill} application?",
        "Explain the internal architecture of {skill}.",
        "How does {skill} handle concurrency or scalability?",
        "Design a system using {skill} for a high-traffic application.",
        "What are the security concerns when using {skill}?",
    ],
    'behavioral': [
        "Tell me about a time you learned {skill} quickly for a deadline.",
        "How do you stay updated with the latest {skill} trends?",
        "Describe a team project where you used {skill}.",
        "Tell me about a failure you had while working with {skill}.",
        "How would you teach {skill} to a junior developer?",
    ],
    'general': [
        "Tell me about yourself.",
        "Why should we hire you?",
        "What are your strengths and weaknesses?",
        "Where do you see yourself in 5 years?",
        "Why do you want to work with our company?",
        "Tell me about a project you're most proud of.",
        "How do you handle pressure and tight deadlines?",
        "Describe your ideal work environment.",
        "What motivates you as a developer?",
        "Do you have any questions for us?",
    ]
}