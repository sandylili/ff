from flask_wtf  import  Form
from wtforms import StringField, TextAreaField, BooleanField, SelectField,\
    SubmitField,FileField,FieldList,FormField
from wtforms.validators import DataRequired, Length, Email, Regexp,Required
from wtforms import ValidationError
from flask_pagedown.fields import PageDownField

from flask_wtf.file import FileField

class searchForm(Form):
    name = StringField(u'商品名称?')
    id = StringField('What is goodsid?')
    storehome = StringField('What is goodshome?')
    
    submit = SubmitField('Submit')
 
class addgood(Form):
    name = StringField('What is goodsname?')
    id = StringField('What is goodsid?', validators=[Required()])
    unit = StringField('What is goodsunit?')
    model = StringField('What is goodsmodel?')
    submit = SubmitField('Submit')

class addstorehome(Form):
    name = StringField('What is storename?')
    id = StringField('What is storeid?')


class authinoroutForm(Form):
    name = StringField('What is goodsname?')
    id = StringField('What is goodsid?', validators=[Required()])
    storehome = StringField('What is goodshome?', validators=[Required()])
   
    number = StringField('What is goodsnmber?')
    
    submit = SubmitField('Submit')

class inoroutForm(Form):
    
    id = StringField('What is goodsid?', validators=[Required()])
    name = StringField('What is goodsname?')
    number = StringField('What is goodsnmber?')

   
    submit = SubmitField('Submit')


class bForm(Form):
    
    
    idd = StringField('What is goodsid?', validators=[Required()])
    cnn = StringField('What is goodsname?')
    number = StringField('What is goodsnmber?')
   
    
class AddForm(Form):
    item_list = FieldList(FormField(bForm),min_entries =2)
    submit = SubmitField('Submit')
    submit1 = SubmitField('add')
    submit2 = SubmitField('due')
    
    

                         
class filegood(Form):
    wenjianname = FileField('What is filesname?')
    
    submit = SubmitField('Submit')


    
    

from werkzeug import secure_filename
from flask_wtf.file import FileField

class PhotoForm(Form):
    photo = FileField('Your photo')
    submit = SubmitField('Submit')




