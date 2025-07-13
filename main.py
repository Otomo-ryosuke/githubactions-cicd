import functions_framework


@functions_framework.http
def github_actions_cicd(request):
    """Cloud Run Functions のメイン関数"""
    print("Hello world")
    return "finish"
