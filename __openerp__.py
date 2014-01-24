{
    'name' : "Project FiFo",
    'version' : "1.0",
    'author' : "Arda Xi",
    'category' : "Tools",
    'depends' : [],
    'external_dependencies': {'python': ['fifo']},
    'data' : [
        'web_fifo_view.xml',
        'web_fifo_server_view.xml',
        'res_users_view.xml',
    ],
    'js': ['static/src/js/*.js'],
    'qweb': ['static/src/xml/*.xml'],
    'installable': True,
}