
from flask import render_template, redirect, url_for, abort, flash, request,\
    current_app, make_response
from flask_login import login_required, current_user
from flask_sqlalchemy import get_debug_queries
from . import main
from .forms import searchForm, inoroutForm,addgood,addstorehome,filegood,PhotoForm

from .. import db

from ..models import Good,Number,InOut,Storehouse


from datetime import datetime

from ..decorators import permission_required,admin_required


@main.route('/')
def index():
    form = searchForm()
    return render_template('index.html', form=form)


@main.route('/search',methods=['GET', 'POST'])
def search():
    form = searchForm()
    number=[]
    if form.validate_on_submit():
       if form.id.data:
            
            good=Good.query.filter_by(goodid=form.id.data).first()
            number=Number.query.filter_by(good=good).all()
            return render_template('search.html', form=form,number=number)
       else:
            
            good=Good.query.filter_by(goodname=form.name.data).all()
            
            c=[]
            for a in good:
                
                b=Number.query.filter_by(good=a).all()
                c.append(b)
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
@permission_required(0)
def outgoods():
    form = inoroutForm()
    a=[]
    if form.validate_on_submit():
        if form.id.data:
            a=Number.query.filter_by(good_id=form.id.data,storehouse_id=form.storehome.data).first()
            if not form.number.data:
                form.number.data=0
            
            
            a.nownumber=a.nownumber-float(form.number.data)
            a.changedate= datetime.utcnow()
            b=InOut(good_id=a.good_id,storehouse_id=a.storehouse_id,changenumber=form.number.data,inorout=True)

            
            db.session.add_ll([a,b])
            db.session.commit()
            return render_template('ingoods.html', form=form,a=a)
        
    return render_template('ingoods.html', form=form,a=a)


@main.route('/filegoods',methods=['GET', 'POST'])
def filegoods():
    form = filegood()
    if form.validate_on_submit():
        file = form.wenjianname.data
        
        file.save(file.filename )
        import xlrd
        data = xlrd.open_workbook(file.filename)
        table = data.sheets()[0]
        nrows = table.nrows
        for i in range(1,nrows):
            a=table.row_values(i, start_colx=0, end_colx=None)
            c=Good(goodid = int(a[0]),goodname=a[1],goodunit=a[2],goodmodel=a[3])
            db.session.add(c)
            db.session.commit()
            
            
        

        
        return render_template('filegood.html', fom=form)
    return render_template('filegood.html', fom=form)


