from datetime import timedelta

from django.contrib.auth import get_user_model
from django.test import TestCase
from django.utils import timezone
from rest_framework.test import APIClient

from repairs.models import WorkOrder


class TrendDataAPITests(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user_model = get_user_model()
        self.admin = self.user_model.objects.create_user(
            username='admin_test',
            password='admin123',
            role=3,
        )
        self.student = self.user_model.objects.create_user(
            username='student_test',
            password='student123',
            role=1,
        )
        self.client.force_authenticate(user=self.admin)

    def test_trend_data_counts_completed_without_finish_time(self):
        """
        status=3 但 finish_time 为空的历史数据，趋势图应按 create_time 兜底计入 completed。
        """
        create_dt = timezone.now() - timedelta(days=2)
        order = WorkOrder.objects.create(
            user=self.student,
            category='水电',
            priority='medium',
            content='测试工单',
            status=3,
            finish_time=None,
        )
        WorkOrder.objects.filter(pk=order.pk).update(create_time=create_dt, finish_time=None)

        resp = self.client.get('/api/repairs/work-orders/trend_data/', {'range': 'week'})
        self.assertEqual(resp.status_code, 200)
        payload = resp.json()
        self.assertTrue(any((row.get('completed') or 0) > 0 for row in payload))

    def test_trend_data_fallback_to_active_days_when_window_all_zero(self):
        """
        当近一周窗口无数据时，接口会回退到最近活跃日期，避免整段全 0。
        """
        create_dt = timezone.now() - timedelta(days=120)
        order = WorkOrder.objects.create(
            user=self.student,
            category='家具',
            priority='low',
            content='旧工单',
            status=1,
        )
        WorkOrder.objects.filter(pk=order.pk).update(create_time=create_dt)

        resp = self.client.get('/api/repairs/work-orders/trend_data/', {'range': 'week'})
        self.assertEqual(resp.status_code, 200)
        payload = resp.json()
        self.assertTrue(any((row.get('submitted') or 0) > 0 for row in payload))

    def test_trend_data_year_aggregates_by_month(self):
        """
        近一年应按“月”聚合，每个点代表整月数据。
        """
        now = timezone.now()
        this_month_dt = now - timedelta(days=3)
        prev_month_dt = now - timedelta(days=35)

        order1 = WorkOrder.objects.create(
            user=self.student,
            category='水电',
            priority='medium',
            content='本月工单',
            status=1,
        )
        WorkOrder.objects.filter(pk=order1.pk).update(create_time=this_month_dt)

        order2 = WorkOrder.objects.create(
            user=self.student,
            category='家具',
            priority='low',
            content='上月工单',
            status=3,
            finish_time=prev_month_dt,
        )
        WorkOrder.objects.filter(pk=order2.pk).update(
            create_time=prev_month_dt,
            finish_time=prev_month_dt,
        )

        resp = self.client.get('/api/repairs/work-orders/trend_data/', {'range': 'year'})
        self.assertEqual(resp.status_code, 200)
        payload = resp.json()
        self.assertEqual(len(payload), 12)
        self.assertTrue(all(len((row.get('date') or '').split('-')) == 3 for row in payload))
        self.assertTrue(any((row.get('submitted') or 0) > 0 for row in payload))
        self.assertTrue(any((row.get('completed') or 0) > 0 for row in payload))
