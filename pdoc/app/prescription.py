from docx.shared import Cm
from docxtpl import DocxTemplate, InlineImage

context = {
    
    'date': '30 Mar',
    'doctor_id': '12345567689',
    'medicines': [
        {
            'sl': '1',
            'name': 'Medicine 1',
            'morning': 'After Food',
            'noon': 'After Food',
            'night' : 'NO',
            'evening' : 'NO',
        }, {
            'sl': '2',
            'name': 'Medicine 1',
            'morning': 'After Food',
            'noon': 'After Food',
            'night' : 'NO',
            'evening' : 'NO',
        }, {
            'sl': '3',
            'name': 'Medicine 1',
            'morning': 'After Food',
            'noon': 'After Food',
            'night' : 'NO',
            'evening' : 'NO',
        }
    ]
}
tpl = DocxTemplate("template.docx")
tpl.render(context)
tpl.save('dynamic_table.docx')
