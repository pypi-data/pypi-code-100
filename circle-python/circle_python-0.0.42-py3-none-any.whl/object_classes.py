import circle
from circle import resources

OBJECT_CLASSES = {
    resources.Ach.OBJECT_NAME: resources.Ach,
    resources.Balances.OBJECT_NAME: resources.Balances,
    resources.Card.OBJECT_NAME: resources.Card,
    resources.MasterWallet.OBJECT_NAME: resources.MasterWallet,
    resources.Message.OBJECT_NAME: resources.Message,
    resources.MocksAchAccount.OBJECT_NAME: resources.MocksAchAccount,
    resources.MockWirePayment.OBJECT_NAME: resources.MockWirePayment,
    resources.Notification.OBJECT_NAME: resources.Notification,
    resources.Payment.OBJECT_NAME: resources.Payment,
    resources.Payout.OBJECT_NAME: resources.Payout,
    resources.Settlement.OBJECT_NAME: resources.Settlement,
    resources.Subscription.OBJECT_NAME: resources.Subscription,
    resources.Wire.OBJECT_NAME: resources.Wire,
    resources.WireInstruction.OBJECT_NAME: resources.WireInstruction,
}
