{
    'name': 'Internship Management',
    'version': '1.0',
    'summary': 'Manage academic internships',
    'description': 'A module to manage students, companies, internships, and reports.',
    'author': 'Bechir Ben Tekfa',
    'category': 'Education',
    'icon': 'static/description/icon.png',
    'depends': [
        'base',
        'mail',
        'board',
        'web',
    ],
    'data': [
        'security/ir.model.access.csv',
        'report/convention_report.xml',
        'views/student_views.xml',
        'views/company_views.xml',
        'views/internship_views.xml',
        'views/report_views.xml',
        'views/application_views.xml',
        'views/dashboard_views.xml',
        'views/menus.xml',
        'data/email_templates.xml',
    ],
    'demo': [
        'demo/demo_data.xml',
    ],
    'assets': {
        'web.assets_backend': [
            'internship_management/static/src/js/internship_dashboard.js',
            'internship_management/static/src/css/dashboard.css',
            'internship_management/static/src/css/internship_dashboard.css',
        ],
        'web.assets_qweb': [
            'internship_management/static/src/xml/dashboard_templates.xml',
        ],
    },
    'installable': True,
    'application': True,
    'license': 'LGPL-3',
}