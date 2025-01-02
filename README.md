# sh7n-dev4

週7日本語 Developmentプロジェクト4

# ワークフロー
## Workersプロジェクト作成まで

```zsh
cd ~/dev
npm install wrangler --save-dev     # wranglerをdevディレクトリにインストール
npx wrangler login                  # Cloudflareログイン
npm create cloudflare@latest        # Workersプロジェクトを作成
# ↑の質問への回答:
#   In which directory do you want to create your application?  -> ./sh7n-dev4
#   What would you like to start with?                          -> Hello World example
#   Which template would you like to use?                       -> Hello World Worker
#   Which language do you want to use?                          -> TypeScript
#   Do you want to use git for version control?                 -> Yes
#   Do you want to deploy your application?                     -> No
```

## Workers Site作成まで

参考: https://developers.cloudflare.com/workers/configuration/sites/start-from-worker/

### 1. ローカルで以下のコマンドを実行

```zsh
vi wrangler.toml    # wrangler.tomlに追記
# ↓を追記
# # Workers Site
# # 参考 https://developers.cloudflare.com/workers/configuration/sites/start-from-worker/
# [site]
# bucket = "./public" # the directory with your static assets
npm install @cloudflare/kv-asset-handler --save-dev     # kv-asset-handlerをdevディレクトリにインストール
SH7N_DEV_CONFIG=$HOME/dev/sh7n-bundle/sh7n-dev3
cp -r $SH7N_DEV_CONFIG/static \
      $SH7N_DEV_CONFIG/templates \
      $SH7N_DEV_CONFIG/docker-compose.yaml \
      $SH7N_DEV_CONFIG/Dockerfile \
      $SH7N_DEV_CONFIG/main.dev1.py \
      $SH7N_DEV_CONFIG/main.py \
      $SH7N_DEV_CONFIG/Makefile \
      $SH7N_DEV_CONFIG/requirements.txt .
mv main.dev1.py main.dev.1.py   # 名称変更
mkdir .github/workflows                       # ディレクトリ作成
vi .github/workflows/daily-build-trigger.yml  # ファイル作成(内容は略)
vi src/index.ts                               # ファイル編集(内容は略)
vi .dev.vars                                  # ファイル作成(内容は略)
vi docker-compose.dev.1.yaml                  # ファイル作成(内容は略)
vi docker-compose.yaml                        # ファイル編集(内容は略)
vi Makefile                                   # ファイル編集(内容は略)
vi requirements.dev.1.txt                     # ファイル作成(内容は略)
vi Taskfile.yml                               # ファイル作成(内容は略)
npx wrangler deploy     # 初めてのデプロイ
                        # (手早くリモート上にプロジェクトを作成するために一度だけ実行。
                        #  ただし、シークレットが未登録のためデプロイは失敗するだろう。
                        #  以降はこのようなローカルからのデプロイはしない)
```

### 2. ダッシュボードで以下の作業を行う

ダッシュボードの「設定」で以下の設定を行う
```yaml
変数とシークレット:
    - タイプ: シークレット
      名前: SH7N_PASSWORD
      値: 値が暗号化されました  # 注 適切な値に変更すること。以降も同様。
    - タイプ: シークレット
      名前: SH7N_USER
      値: 値が暗号化されました

ビルド(ベータ版):
    Git リポジトリ: ky5bass/sh7n-dev4
    ビルド構成:
        ビルド コマンド: make build
        デプロイ コマンド: npx wrangler deploy
        ルート ディレクトリ: /
    ブランチ コントロール:
        プロダクション ブランチ: main
    監視パスを構築する:
        パスを含む: *
    API トークン:
        名前: Workers Builds - 2024-12-10 01:17
    変数とシークレット:
        - タイプ: シークレット
          名前: SUPABASE_KEY
          値: 値が暗号化されました
        - タイプ: シークレット
          名前: SUPABASE_URL
          値: 値が暗号化されました
    ビルド キャッシュ: 無効
```

**2025/1/3追記 現時点では↑のとおりではなく、デプロイ回数削減のためにGitリポジトリとの接続を解除している**

## Gitクローンから始める場合

```zsh
git clone git@github.com:ky5bass/sh7n-dev4.git  # Gitクローン
cd sh7n-dev4
npm ci
vi .dev.vars
task gen
```