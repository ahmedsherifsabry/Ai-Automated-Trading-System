# controllers/trade_controller.py

from services.signal_service import SignalService


def list_pending(limit: int = 20, only_pending: bool = True):
    return SignalService.list_pending(limit, only_pending)


def approve(signal_id: int):
    SignalService.update_status(signal_id, 'APPROVED')


def reject(signal_id: int):
    SignalService.update_status(signal_id, 'REJECTED')
