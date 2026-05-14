from flask import Blueprint, render_template, request, redirect, url_for, flash
from app.models.task import TaskModel

task_bp = Blueprint('task', __name__)

@task_bp.route('/')
def index():
    """
    顯示所有任務。可接收 ?status= 參數進行過濾。
    """
    pass

@task_bp.route('/tasks/add', methods=['POST'])
def add():
    """
    接收表單 title，新增任務，成功後重導向 /
    """
    pass

@task_bp.route('/tasks/<int:id>/toggle', methods=['POST'])
def toggle(id):
    """
    更新特定 ID 的狀態，成功後重導向 /
    """
    pass

@task_bp.route('/tasks/<int:id>/edit', methods=['GET', 'POST'])
def edit(id):
    """
    GET: 顯示特定任務的修改表單
    POST: 接收表單修改後的 title，更新後重導向 /
    """
    pass

@task_bp.route('/tasks/<int:id>/delete', methods=['POST'])
def delete(id):
    """
    刪除特定 ID 的任務，成功後重導向 /
    """
    pass
