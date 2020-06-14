from core.app import Response, JsonResponse
from core.shortcuts import redirect
from core.views import TemplateView, View
from server.apps.comments.services import (
    get_cities,
    delete_comment,
    get_comment_view_content,
    get_statistic_content, check_validate_form_data, insert_comment, get_comment_add_content
)


class IndexView(TemplateView):
    """
    Просмотр главной страницы.
    """
    template_name = "index.html"


class CommentAddView(TemplateView):
    """
    Форма для добавления комментария
    """
    template_name = "comment.html"

    def get(self, request, *args, **kwargs):
        return Response(body=get_comment_add_content(template_name=self.template_name))

    def post(self, request, *args, **kwargs):
        if check_validate_form_data(request.POST):
            insert_comment(comment=request.POST)
        return redirect('/view')


class StatisticView(TemplateView):
    """
    Просмотр статистики по регионам и городам
    """

    template_name = 'stat.html'

    def get(self, request, *args, **kwargs):
        if "id" in request.GET:
            region_id = int(request.GET['id'][0])
            return Response(body=get_statistic_content(template_name=self.template_name,
                                                       region_id=region_id))
        elif request.path == "/stat":
            return Response(body=get_statistic_content(template_name=self.template_name))


class CommentView(TemplateView):
    """
    Просмотр списка комментариев
    """
    template_name = "view.html"

    def get(self, request, *args, **kwargs):
        return Response(body=get_comment_view_content(template_name=self.template_name))


class DeleteComment(View):
    """
    API view для удаления комментария
    """

    def post(self, request, *args, **kwargs):
        if delete_comment(request.POST["id"][0]):
            return JsonResponse(body={"delete": "success"})
        else:
            raise JsonResponse(body={"delete": "error"}, status="400 Bad Request")


class RegionView(View):
    """
    API view для получения списка городов
    """

    def post(self, request, *args, **kwargs):
        return JsonResponse(body=get_cities(region_id=request.POST['id'][0]))
