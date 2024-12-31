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

```zsh
vi wrangler.toml    # wrangler.tomlに追記
# ↓を追記
# # Workers Site
# # Docs: https://developers.cloudflare.com/workers/configuration/sites/start-from-worker/
# [site]
# bucket = "./public" # the directory with your static assets
npm install @cloudflare/kv-asset-handler --save-dev     # kv-asset-handlerをdevディレクトリにインストール
npx wrangler deploy
```