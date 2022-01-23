# 설치 / 실행

## 1. 의존성

의존성 관리는 [Poetry](https://python-poetry.org/docs/) 으로 관리됩니다. 프로젝트 경로에서 아래 명령어를 입력해 프로젝트에 필요한 의존성을 설치 할 수 있습니다.

```bash
# (프로젝트 경로에서)
$ poetry install
$ poetry shell
```

## 2. vscode 통합

### (1)_커맨드 팔레트 여는 법_

- Window: ctrl + shift + p
- Mac: command + shift + p

### (2) 가상환경 선택

`poetry shell` 명령어로 가상환경이 생성되었다면 커맨드 팔레트를 열어 `Python: Select Interpreter` 를 클릭합니다.
그리고 생성된 가상환경 주소를 입력 또는 클릭합니다

### (3) 린트, 포멧터 설정

커맨드 팔레트를 열어서 `Open Workspace Settings (Json)` 을 클릭하고 아래 json 코드를 적습니다.

```json
{
  "python.linting.enabled": true,
  "python.linting.flake8Enabled": true,

  "python.formatting.provider": "black",

  "[python]": {
    "editor.formatOnSave": true,
    "editor.codeActionsOnSave": {
      "source.organizeImports": true,
      "python.sortImports": true
    }
  }
}
```

## 3. 환경변수

export 명령을 이용하여 직접 환경변수를 설정하거나 최상위 디렉터리에 .env 파일을 생성하여 환경변수를 설정할 수 있습니다.

```ini
# 환경변수 설정
SECRET_KEY="secret key"
ALLOWED_HOSTS="*"
```

또는

```bash
# linux 환경변수 설정
$ export SECRET_KEY="secret key"
$ export ALLOWED_HOSTS="example-domain.com,example-domain2.com"
```

## 4. 프로젝트 실행

```bash
(가상환경) $ python manage.py migrate
(가상환경) $ python manage.py runserver
```
