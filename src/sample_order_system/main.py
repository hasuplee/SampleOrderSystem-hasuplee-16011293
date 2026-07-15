"""반도체 시료 생산주문관리 시스템 - 콘솔 진입점."""
import argparse
import sys

from sample_order_system.controller.main_controller import MainController
from sample_order_system.model.production_queue import ProductionQueue
from sample_order_system.repository.order_repository import OrderRepository
from sample_order_system.repository.production_job_repository import ProductionJobRepository
from sample_order_system.repository.sample_repository import SampleRepository
from sample_order_system.service.approval_service import ApprovalService
from sample_order_system.service.monitoring_service import MonitoringService
from sample_order_system.service.order_service import OrderService
from sample_order_system.service.production_service import ProductionService
from sample_order_system.service.shipment_service import ShipmentService


def main() -> None:
    if sys.stdout.encoding.lower() != "utf-8":
        sys.stdout.reconfigure(encoding="utf-8")
        sys.stdin.reconfigure(encoding="utf-8")

    parser = argparse.ArgumentParser(description="반도체 시료 생산주문관리 시스템")
    parser.add_argument("--db", default="sample_order.db", help="SQLite DB 파일 경로")
    args = parser.parse_args()

    sample_repository = SampleRepository(args.db)
    order_repository = OrderRepository(args.db)
    production_job_repository = ProductionJobRepository(args.db)
    production_queue = ProductionQueue()

    controller = MainController(
        sample_repository=sample_repository,
        order_repository=order_repository,
        order_service=OrderService(sample_repository, order_repository),
        approval_service=ApprovalService(
            sample_repository, order_repository, production_queue, production_job_repository,
        ),
        monitoring_service=MonitoringService(sample_repository, order_repository),
        production_service=ProductionService(
            sample_repository, order_repository, production_queue, production_job_repository,
        ),
        production_queue=production_queue,
        shipment_service=ShipmentService(order_repository),
    )
    controller.run()


if __name__ == "__main__":
    main()
