# sh7n-dev4

週7日本語 Developmentプロジェクト4

# ワークフロー(Workersプロジェクト作成まで)

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