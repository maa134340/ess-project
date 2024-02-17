from pytest_bdd import parsers, given, when, then, scenario
from service.review_service import ReviewService

@scenario(scenario_name='Cadastrar um review com sucesso', feature_name='../features/review.feature')
def test_cadastrar_um_review_com_sucesso():
    pass

@given(parsers.cfparse('o usuário "{username}" não tem um review cadastrado para a disciplina "{discipline}"'))
def delete_user(username: str, discipline: str):

    existing_reviews = ReviewService.get_reviews_by_name_and_discipline(discipline, username)

    for review in existing_reviews:
        id_to_delete = review['_id']
        removed_id = ReviewService.delete_review(id_to_delete)
    
@when(
    parsers.cfparse('uma requisição POST é enviada "{url}" com username "{username}", disciplina "{discipline}", nota "{rating}" e comentário "{comment}"'),
    target_fixture="context"
)
def add_review(client, context, url: str, username: str, discipline: str, rating: int, comment: str):
    # try route
    response = client.post(url, json={"username": username, "discipline": discipline, "rating": rating, "comment": comment})
    context["response"] = response
    
    # remove review if it exists
    existing_reviews = ReviewService.get_reviews_by_name_and_discipline(discipline, username)
    if(len(existing_reviews) != 0):
        id_to_delete = existing_reviews[0]['_id']
        removed_id = ReviewService.delete_review(id_to_delete)

    return context

@then(
    parsers.cfparse('o código da resposta é "{response_code}"'),
    target_fixture="response_code"
)
def check_response_status_code(context, response_code: str):
    assert context["response"].status_code == int(response_code)

@then(parsers.cfparse('o JSON da resposta deve conter username "{username}", disciplina "{discipline}", nota "10" e comentário "{comment}"'))
def response_json(context, username: str, discipline: str, comment: str):
    response_json = context["response"].json()
    assert response_json["username"] == username
    assert response_json["discipline"] == discipline
    assert response_json["rating"] == 10
    assert response_json["comment"] == comment