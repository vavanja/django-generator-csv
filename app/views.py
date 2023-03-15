import os
import time
from datetime import date

import botocore
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from django.forms import modelformset_factory
from django.http import JsonResponse
from django.core.files.storage import FileSystemStorage

import csv
import boto3
import io

from .models import DataSchema, User, Column, FileName
from .forms import DataSchemaForm, ColumnForm
from Generator_csv.settings import AWS_ACCESS_KEY_ID, AWS_SECRET_ACCESS_KEY


def index(request):
    data_schemas = DataSchema.objects.filter(user_id=request.user.id)
    # data_schemas = DataSchema.objects.all()
    return render(request, 'index.html', {'data_schemas': data_schemas})


@login_required(login_url='login')
def create_schema(request):
    form = DataSchemaForm(request.POST or None)

    context = {
        "form": form,
    }

    if form.is_valid():
        obj = form.save(commit=False)
        obj.user_id_id = request.user.id
        obj.save()
        context_new = {
            'form': form,
            'object': obj
        }
        return render(request, 'create_schema.html', context_new)
        # return render(request, 'forms.html', context_new)

    return render(request, 'create_schema.html', context)


@login_required(login_url='login')
def update_schema(request, pk):
    obj = get_object_or_404(DataSchema, id=pk, user_id=request.user)
    columns = Column.objects.filter(data_schema=pk).all()

    form = DataSchemaForm(request.POST or None, instance=obj)
    ColumnFormSet = modelformset_factory(Column, form=ColumnForm, extra=0)
    qs = obj.column_set.all()
    formset = ColumnFormSet(request.POST or None, queryset=qs)
    context = {
        'form': form,
        'formset': formset,
        'object': obj,
        'columns': columns
    }

    if all([form.is_valid(), formset.is_valid()]):
        parent = form.save(commit=False)
        parent.save()
        for form in formset:
            child = form.save(commit=False)
            child.data_schema = parent
            child.save()

        context['message'] = 'Data saved'
    if request.htmx:
        return render(request, 'forms.html', context)
    return render(request, 'update_schema.html', context)


@login_required(login_url='login')
def delete_schema(request, pk):
    schema = DataSchema.objects.get(id=pk)
    if request.method == 'POST':
        schema.delete()
        return redirect('/')
    context = {'schema': schema}
    return render(request, 'delete_schema.html', context)


@login_required(login_url='login')
def delete_column(request, pk, col_name):
    # pk - schema.id

    column = get_object_or_404(Column, name=col_name, data_schema=pk)
    if column:
        column.delete()
        return redirect(f'/update/{pk}')

    return redirect('/')


def is_ajax(request):
    return request.META.get('HTTP_X_REQUESTED_WITH') == 'XMLHttpRequest'


def export_to_csv(request, pk):
    obj = get_object_or_404(DataSchema, id=pk, user_id=request.user)
    qs = obj.column_set.all()

    if is_ajax(request):
        num_rows = int(request.POST.get('num_rows'))
        csvfile = io.StringIO()

        writer = csv.writer(csvfile)
        fieldnames = [col.name for col in qs]
        writer.writerow(fieldnames)

        col_type = [col.data_type for col in qs]

        fake_data = {
            'Full name': 'Hanna Montana',
            'Job': 'Software Engineer',
            'Email': 'example@gmail.com',
            'Phone number': '+1234567890',
            'Date': date.today()
        }

        for i in range(num_rows):
            row = []
            for column in col_type:
                if column == 'Full name':
                    row.append(fake_data[column])
                elif column == 'Job':
                    row.append(fake_data[column])
                elif column == 'Email':
                    row.append(fake_data[column])
                elif column == 'Phone number':
                    row.append(fake_data[column])
                elif column == 'Date':
                    row.append(fake_data[column])
            writer.writerow(row)
        # print(csvfile)
        file_storage = FileSystemStorage()
        file_name = f'{obj.name}.csv'
        root_path = os.getcwd()
        if os.path.join(root_path, 'media', file_name):
            file_name = f'{obj.name}{num_rows}.csv'
        filename = file_storage.save(file_name, csvfile)

        bucketName = 'csvfilebucket1'
        client = boto3.client('s3', aws_access_key_id=AWS_ACCESS_KEY_ID,
                              aws_secret_access_key=AWS_SECRET_ACCESS_KEY)

        file_path = os.path.join(root_path, 'media', file_name)
        s3 = boto3.client('s3', aws_access_key_id=AWS_ACCESS_KEY_ID,
                          aws_secret_access_key=AWS_SECRET_ACCESS_KEY)
        try:
            check = client.head_object(Bucket=bucketName, Key=file_name)
            if check:
                file_name = f'{obj.name}{num_rows}.csv'
                client.upload_file(file_path, bucketName, file_name, ExtraArgs={'ACL': 'public-read'})
        except botocore.exceptions.ClientError as e:
            if e.response['Error']['Code'] == "404":
                client.upload_file(file_path, bucketName, file_name, ExtraArgs={'ACL': 'public-read'})
            else:
                print('Error', e)

        location = s3.get_bucket_location(Bucket=bucketName)[
            'LocationConstraint']
        location_url = "https://s3-%s.amazonaws.com/%s/%s" % (location, bucketName, file_name)
        file = FileName.objects.create(status='Ready', download_link=location_url, schema_id=obj,
                                       user_id=request.user)
        # data = {
        #     'download_link': location_url,
        #     'status': 'Ready',
        #     'date': date.today()
        # }
        data = {
            'download_link': file.download_link,
            'status': file.status,
            'date': file.date_created
        }
        time.sleep(2.5)
        return JsonResponse(data)


def dataset(request, pk):
    obj = get_object_or_404(DataSchema, id=pk, user_id=request.user)
    qs = obj.column_set.all()
    datasets = FileName.objects.filter(schema_id=obj, user_id=request.user).all()
    context = {
        'object': obj,
        'queryset': qs,
        'download_link': '',
        'datasets': datasets,
        'status': 'Processing',

    }
    return render(request, 'csv_generator.html', context)
