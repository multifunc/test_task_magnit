from core.router import Router
from server.apps.comments.views import IndexView, CommentAddView, StatisticView, CommentView, RegionView, DeleteComment

router = Router(__file__)

router.add_route(r'^/$', IndexView())
router.add_route(r'^/index$', IndexView())
router.add_route(r'^/comment$', CommentAddView())
router.add_route(r'^/stat$', StatisticView())
router.add_route(r'^/stat?id=\d*', StatisticView())
router.add_route(r'^/view$', CommentView())
router.add_route(r'^/comment/delete$', DeleteComment())
router.add_route(r'^/region$', RegionView())

