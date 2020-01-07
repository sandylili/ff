
from flask import render_template, redirect, url_for, abort, flash, request,\
    current_app, make_response
from flask_login import login_required, current_user
from flask_sqlalchemy import get_debug_queries
from . import main
from .forms import searchForm, inoroutForm,addgood,addstorehome,filegood,PhotoForm,AddForm

from .. import db

from ..models import Good,Number,InOut,Storehouse,User


from datetime import datetime

from ..decorators import permission_required,admin_required

import os,requests, json


@main.route('/')
def index():
    response = requests.get('http://t.weather.sojson.com/api/weather/city/101110101')
    d = response.json()
    return render_template('index.html', d=d)

@main.route('/authsearch',methods=['GET', 'POST'])
def authsearch():
    form = searchForm()
    number=[]
    if form.validate_on_submit():
       if form.id.data:
            
            good=Good.query.filter_by(goodid=form.id.data).first()
            
            number=Number.query.filter_by(good=good).all()
            
            form.id.data=None
            form.name.data=None
            form.storehome.data=None
            
            return render_template('search.html', form=form,number=number)
        
       else:
            
            good=Good.query.filter(Good.goodname.like("%" + form.name.data + "%")).all()
            
            c=[]
            for a in good:
                
                b=Number.query.filter_by(good=a).all()
                c.append(b)

            form.id.data=None
            form.name.data=None
            form.storehome.data=None
            return render_template('namesearch.html', form=form,c=c)
             
    return render_template('search.html', form=form,number=number)



@main.route('/search',methods=['GET', 'POST'])
@login_required
def search():
    form = searchForm()
    number=[]
    if form.validate_on_submit():
       if form.id.data:
            
            good=Good.query.filter_by(goodid=form.id.data).first()
            if current_user.id == 1 :
                number=Number.query.filter_by(good=good,storehouse_id=current_user.id).all()
            
                
            form.id.data=None
            form.name.data=None
            form.storehome.data=None
            
            return render_template('search.html', form=form,number=number)
        
       else:
            
            good=Good.query.filter(Good.goodname.like("%" + form.name.data + "%")).all()
            
            c=[]
            for a in good:
                
                b=Number.query.filter_by(good=a,storehouse_id=current_user.id).all()
                c.append(b)

            form.id.data=None
            form.name.data=None
            form.storehome.data=None
            return render_template('namesearch.html', form=form,c=c)
             
    return render_template('search.html', form=form,number=number)



@main.route('/namesearch',methods=['GET', 'POST'])
def namesearch():
    form = searchForm()
    if form.validate_on_submit():
        good=Good.query.filter_by(goodname='shi').all()
        return render_template('namesearch2.html', form=form,c=good)
    return render_template('namesearch.html', form=form,c=0)
            
             
    


@main.route('/addgood',methods=['GET', 'POST'])
@admin_required
def addgoods():
    form = addgood()
    if form.validate_on_submit():
        name = form.name.data  
        id = form.id.data
        unit=form.unit.data
        model = form.model.data

        a=Good(goodid = int(id),goodname=name,goodunit=unit,goodmodel=model)  
        db.session.add(a)
        db.session.commit()

        form.id.data = ''
        flash('congratuation!!')
        
        return render_template('addgood.html', form=form,goods=a)
    return render_template('addgood.html', form=form,goods=0)
    

@main.route('/ingoods',methods=['GET', 'POST'])
@admin_required
def ingoods():
    form = inoroutForm()
    a=[]
    
    if form.validate_on_submit():
        if form.id.data:
            a=Number.query.filter_by(good_id=form.id.data,storehouse_id=form.storehome.data).first()
            if not form.number.data:
                form.number.data=0
            a.nownumber=a.nownumber+float(form.number.data)
            db.session.add(a)
            db.session.commit()
            return render_template('ingoods.html', form=form,a=a)
        
    return render_template('ingoods.html', form=form,a=a)
        
@main.route('/outgoods',methods=['GET', 'POST'])
def outgoods():
    form = AddForm()
    c=[]
    if form.submit1.data:
        
        form.item_list.append_entry()
    elif form.submit2.data:
        form.item_list.pop_entry()
    elif form.submit.data:
        for i in form.item_list:
            if i.idd.data and i.number.data :
                a=Number.query.filter_by(good_id=i.idd.data,storehouse_id=current_user.id).first()
                if not a:
                    flash('not %s!'%i.idd.data)
                    i.idd.data=None
                    i.number.data =None
                    i.cnn.data =None
                    
                    continue
                    
                if a.nownumber-float(i.number.data)>=0:
                    a.nownumber=a.nownumber-float(i.number.data)
                    a.changedate= datetime.utcnow()
                    b=InOut(good_id=a.good_id,storehouse_id=a.storehouse_id,changenumber=i.number.data,inorout=True,user=current_user._get_current_object())
                    db.session.add_all([a,b])
                    db.session.commit()
                    c.append([a.good_id,a.storehouse_id,i.number.data,True,current_user._get_current_object().username])
                    flash('congratulation! %s'%i.idd.data)
                    i.idd.data=None
                    i.number.data =None
                    i.cnn.data =None
                    
                    
                else :
                    flash('goods %s number are not enough !'%i.idd.data )
                    
                    
            
        
        return render_template('insgoods.html', form=form,a=c)
            
            
            
              
    return render_template('insgoods.html', form=form,a=c)        
        
'''
@main.route('/outgoods',methods=['GET', 'POST'])
@permission_required(0)
def outgoods():
    form = inoroutForm()
    a=[]
    if form.validate_on_submit():
        if form.id.data:
            a=Number.query.filter_by(good_id=form.id.data,storehouse_id=current_user.id).first()
            if not form.number.data:
                form.number.data=0

            if not a:
                form.id.data=None
                form.name.data=None
                
                form.number.data=None
                
                return render_template('ingoodserro.html', form=form)
            
            if a.nownumber-float(form.number.data)>=0:
                
               a.nownumber=a.nownumber-float(form.number.data)
               a.changedate= datetime.utcnow()
               b=InOut(good_id=a.good_id,storehouse_id=a.storehouse_id,changenumber=form.number.data,inorout=True,user=current_user._get_current_object())      
               db.session.add_all([a,b])
               db.session.commit()
               form.id.data=None
               form.name.data=None
               
               form.number.data=None
               flash('congratulation!')
               return render_template('ingoods.html', form=form,a=a)
            else:
                form.id.data=None
                form.name.data=None
                
                form.number.data=None
                flash('goods number are not enough !')
                return render_template('ingoods.html', form=form,a=a)
        
    return render_template('ingoods.html', form=form,a=a)
'''
def upfile(file,app):
        import xlrd
        data = xlrd.open_workbook(file.filename)
        table = data.sheets()[0]
        nrows = table.nrows
        
        with app.app_context():
         for i in range(1,nrows):
            a=table.row_values(i, start_colx=0, end_colx=None)
            c=Good(goodid = int(a[0]),goodname=a[1],goodunit=a[2],goodmodel=a[3])
            
            db.session.add(c)
            db.session.commit()
            
        table = data.sheets()[1]
        nrows = table.nrows
        with app.app_context():
         for i in range(1,nrows):
            a=table.row_values(i, start_colx=0, end_colx=None)
            c=User(username = a[0],role_id=int(a[1]),password=a[2])
            db.session.add(c)
            db.session.commit()

        table = data.sheets()[2]
        nrows = table.nrows
        with app.app_context():
         for i in range(1,nrows):
            a=table.row_values(i, start_colx=0, end_colx=None)
            c=Storehouse(SHname = a[0])
            db.session.add(c)
            db.session.commit()

        table = data.sheets()[3]
        nrows = table.nrows
        with app.app_context():
         for i in range(1,nrows):
            a=table.row_values(i, start_colx=0, end_colx=None)
            c=Number(good_id = int(a[0]),storehouse_id=int(a[1]),nownumber=int(a[2]))
            db.session.add(c)
            db.session.commit()
            
        os.remove(file.filename)
                
    


@main.route('/filegoods',methods=['GET', 'POST'])
def filegoods():
    form = filegood()
    if form.validate_on_submit():
        file = form.wenjianname.data
        
        file.save(file.filename )
        
        from threading import Thread
        app = current_app._get_current_object()
        thr = Thread(target=upfile, args=[file,app])
        thr.start()
        
            
            
        

        
        return render_template('filegood.html', fom=form)
    return render_template('filegood.html', fom=form)


