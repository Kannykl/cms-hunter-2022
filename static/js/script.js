function ajaxSend(url, params) {
    // Отправляем запрос
    fetch(`${url}?${params}`, {
        method: 'GET',
        headers: {
            'Content-Type': 'application/x-www-form-urlencoded',
        },
    })
        .then(response => response.json())
        .then(json => ren(json))
        .catch(error => console.error(error))
}

const forms = document.querySelector('form[name=search]');

forms.addEventListener('submit', function (e) {
    // Получаем данные из формы
    e.preventDefault();
    let url = this.action;
    let params = new URLSearchParams(new FormData(this)).toString();
    ajaxSend(url, params);
});

function ren(data) {
    // Рендер шаблона
    let  template = Hogan.compile(html);
    let output = template.render(data);
    if (data['cms'].length == 0){
        const alert = document.querySelector('table');
        alert.innerHTML = output;
        } else {
            const table = document.querySelector('tbody');
            table.innerHTML = output;
        }

}

var html = '\
{{#cms}}\
    <tr>\
        <td>\
            {{hostname}}\
        </td>\
        <td>\
            {{cms}}\
        </td>\
        <td>\
            {{vulnerability}}\
        </td>\
        <td>\
            {{github_repository}}\
        </td>\
    </tr>\
{{/cms}}\
{{^cms}}\
<thead>\
    <tr>\
    </tr>\
</thead>\
<tbody>\
</tbody>\
<p class="myalert">По вашему запросу ничего не найдено</p>\
{{/cms}}'
