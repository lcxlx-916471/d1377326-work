from flask import Blueprint, render_template, request, redirect, url_for, flash
from app.models.task import TaskModel

task_bp = Blueprint('task', __name__)

@task_bp.route('/')
def index():
    """
    顯示所有任務。可接收 ?status= 參數進行過濾。
    """
    status_filter = request.args.get('status')
    
    if status_filter in ['0', '1']:
        tasks = TaskModel.get_all(status=int(status_filter))
    else:
        tasks = TaskModel.get_all()
        status_filter = 'all'
        
    return render_template('tasks/index.html', tasks=tasks, current_status=status_filter)

@task_bp.route('/tasks/add', methods=['POST'])
def add():
    """
    接收表單 title，新增任務，成功後重導向 /
    """
    title = request.form.get('title', '').strip()
    if not title:
        flash('任務名稱不能為空白！', 'danger')
    else:
        TaskModel.create(title=title)
        flash('任務新增成功！', 'success')
        
    return redirect(url_for('task.index'))

@task_bp.route('/tasks/<int:id>/toggle', methods=['POST'])
def toggle(id):
    """
    更新特定 ID 的狀態，成功後重導向 /
    """
    if TaskModel.toggle_status(id):
        flash('任務狀態已更新！', 'success')
    else:
        flash('找不到該任務！', 'danger')
        
    # 保留原本的過濾狀態
    status_filter = request.args.get('status', 'all')
    if status_filter != 'all':
        return redirect(url_for('task.index', status=status_filter))
    return redirect(url_for('task.index'))

@task_bp.route('/tasks/<int:id>/edit', methods=['GET', 'POST'])
def edit(id):
    """
    GET: 顯示特定任務的修改表單
    POST: 接收表單修改後的 title，更新後重導向 /
    """
    task = TaskModel.get_by_id(id)
    if not task:
        flash('找不到該任務！', 'danger')
        return redirect(url_for('task.index'))
        
    if request.method == 'POST':
        title = request.form.get('title', '').strip()
        if not title:
            flash('任務名稱不能為空白！', 'danger')
            return render_template('tasks/edit.html', task=task)
            
        TaskModel.update(id, title=title)
        flash('任務更新成功！', 'success')
        return redirect(url_for('task.index'))
        
    return render_template('tasks/edit.html', task=task)

@task_bp.route('/tasks/<int:id>/delete', methods=['POST'])
def delete(id):
    """
    刪除特定 ID 的任務，成功後重導向 /
    """
    if TaskModel.delete(id):
        flash('任務已刪除！', 'success')
    else:
        flash('找不到該任務！', 'danger')
        
    status_filter = request.args.get('status', 'all')
    if status_filter != 'all':
        return redirect(url_for('task.index', status=status_filter))
    return redirect(url_for('task.index'))
