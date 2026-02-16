from rest_framework import permissions


class IsStudent(permissions.BasePermission):
    """学生权限"""
    
    def has_permission(self, request, view):
        return request.user and request.user.is_authenticated and request.user.is_student()


class IsRepairman(permissions.BasePermission):
    """维修人员权限"""
    
    def has_permission(self, request, view):
        return request.user and request.user.is_authenticated and request.user.is_repairman()


class IsAdmin(permissions.BasePermission):
    """管理员权限"""
    
    def has_permission(self, request, view):
        return request.user and request.user.is_authenticated and request.user.is_admin()


class IsOwnerOrAdmin(permissions.BasePermission):
    """工单所有者或管理员权限"""
    
    def has_object_permission(self, request, view, obj):
        # 管理员有所有权限
        if request.user.is_admin():
            return True
        
        # 工单所有者可以查看和修改自己的工单
        if hasattr(obj, 'user'):
            return obj.user == request.user
        
        return False
