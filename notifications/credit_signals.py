"""
Credit workflow signal handlers.
Each signal fires an in-app notification to the appropriate recipients
whenever a key credit lifecycle event occurs.
"""
from django.db.models.signals import post_save
from django.dispatch import receiver
from .utils import send_notification, notify_admins


# ── CreditApplication ─────────────────────────────────────────────────────────

def _wire_credit_application():
    from credit.models import CreditApplication

    @receiver(post_save, sender=CreditApplication)
    def on_credit_application_save(sender, instance, created, **kwargs):
        app = instance

        if created:
            send_notification(
                app.farmer, 'credit_workflow',
                'Application Submitted',
                f'Your credit application {app.reference} has been received and is under review.',
                priority='medium', related_obj=app,
            )
            notify_admins(
                'credit_workflow',
                f'New Credit Application: {app.reference}',
                f'Farmer {app.farmer.get_full_name()} submitted a {app.credit_type} '
                f'application for GHS {app.amount_requested}.',
                priority='medium', related_obj=app,
            )
            return

        if app.status == 'approved':
            send_notification(
                app.farmer, 'credit_workflow',
                'Application Approved ✅',
                f'Your application {app.reference} has been approved! '
                f'We are matching you with an investor.',
                priority='high', related_obj=app,
            )

        elif app.status == 'rejected':
            send_notification(
                app.farmer, 'credit_workflow',
                'Application Not Approved',
                f'Your application {app.reference} was not approved. '
                f'Reason: {app.rejection_reason}',
                priority='high', related_obj=app,
            )

        elif app.status == 'matched' and app.matched_investor:
            send_notification(
                app.matched_investor, 'credit_workflow',
                f'New Investment Opportunity: {app.reference}',
                f'A farmer is seeking {app.credit_type} funding of GHS {app.amount_requested}. '
                f'Review and accept or decline from your Opportunities page.',
                priority='urgent', related_obj=app,
            )
            notify_admins(
                'credit_workflow',
                f'Investor Matched: {app.reference}',
                f'Application {app.reference} matched to {app.matched_investor.get_full_name()}.',
                priority='medium', related_obj=app,
            )


# ── CreditAgreement ───────────────────────────────────────────────────────────

def _wire_credit_agreement():
    from credit.models import CreditAgreement

    @receiver(post_save, sender=CreditAgreement)
    def on_credit_agreement_save(sender, instance, created, **kwargs):
        ag = instance

        if created:
            send_notification(
                ag.farmer, 'credit_workflow',
                'Credit Agreement Ready to Sign 📄',
                f'Agreement {ag.reference} is ready. Please review and sign your contract.',
                priority='high', related_obj=ag,
            )
            if ag.investor:
                send_notification(
                    ag.investor, 'credit_workflow',
                    'Credit Agreement Ready to Sign 📄',
                    f'Agreement {ag.reference} is ready for your signature.',
                    priority='high', related_obj=ag,
                )
            return

        # Farmer just signed — notify investor
        if ag.farmer_signed_at and not ag.investor_signed_at and ag.investor:
            send_notification(
                ag.investor, 'credit_workflow',
                'Farmer Has Signed — Your Turn ✍️',
                f'Farmer has signed agreement {ag.reference}. '
                f'Please sign to proceed to disbursement.',
                priority='high', related_obj=ag,
            )

        # Both parties signed
        if ag.farmer_signed_at and ag.investor_signed_at and ag.status == 'active':
            send_notification(
                ag.farmer, 'credit_workflow',
                'Agreement Fully Signed 🎉',
                f'Both parties have signed agreement {ag.reference}. '
                f'Disbursement will be processed shortly.',
                priority='urgent', related_obj=ag,
            )
            notify_admins(
                'credit_workflow',
                f'Agreement Active: {ag.reference}',
                f'Both parties signed. Please proceed with disbursement.',
                priority='urgent', related_obj=ag,
            )


# ── DisbursementRequest ───────────────────────────────────────────────────────

def _wire_disbursement_request():
    from payments.models import DisbursementRequest

    @receiver(post_save, sender=DisbursementRequest)
    def on_disbursement_request_save(sender, instance, created, **kwargs):
        req = instance

        if created:
            notify_admins(
                'credit_workflow',
                f'Disbursement Request: {req.reference} 💸',
                f'{req.requested_by.get_full_name()} requested GHS {req.amount} '
                f'disbursement for {req.agreement.farmer.get_full_name()}.',
                priority='urgent', related_obj=req,
            )
            if req.agreement.investor:
                send_notification(
                    req.agreement.investor, 'credit_workflow',
                    'Disbursement Requested',
                    f'A disbursement of GHS {req.amount} has been requested '
                    f'for your agreement {req.agreement.reference}.',
                    priority='high', related_obj=req,
                )
            return

        if req.status == 'approved' and req.agreement.investor:
            send_notification(
                req.agreement.investor, 'credit_workflow',
                'Disbursement Approved ✅',
                f'Disbursement of GHS {req.amount} for '
                f'{req.agreement.farmer.get_full_name()} has been approved.',
                priority='urgent', related_obj=req,
            )

        elif req.status == 'rejected' and req.agreement.investor:
            send_notification(
                req.agreement.investor, 'credit_workflow',
                'Disbursement Request Rejected',
                f'Disbursement request {req.reference} was rejected. '
                f'Reason: {req.rejection_reason}',
                priority='high', related_obj=req,
            )


# ── Disbursement (funds actually sent) ───────────────────────────────────────

def _wire_disbursement():
    from payments.models import Disbursement

    @receiver(post_save, sender=Disbursement)
    def on_disbursement_save(sender, instance, created, **kwargs):
        if not created:
            return
        d = instance
        ag = d.agreement

        send_notification(
            ag.farmer, 'credit_workflow',
            'Funds Disbursed 🏦',
            f'GHS {d.amount} has been disbursed via {d.method}. Ref: {d.reference}',
            priority='urgent', related_obj=d,
        )
        if ag.investor:
            send_notification(
                ag.investor, 'credit_workflow',
                'Disbursement Complete',
                f'GHS {d.amount} disbursed to {ag.farmer.get_full_name()}. Ref: {d.reference}',
                priority='high', related_obj=d,
            )
        notify_admins(
            'credit_workflow',
            f'Funds Disbursed: {d.reference}',
            f'GHS {d.amount} disbursed. Agreement: {ag.reference}',
            priority='medium', related_obj=d,
        )


def register_all():
    _wire_credit_application()
    _wire_credit_agreement()
    _wire_disbursement_request()
    _wire_disbursement()
