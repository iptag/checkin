// @grant nodejs
let jsname = $env.JSNAME;
console.log(`⏳ 开始执行 ${jsname}`);
$exec(`node ${jsname}`, {
    cwd: 'script/Shell/checkinpanel',
    timeout: 0,
    // prettier-ignore
    env: {
        NODE_PATH: "/usr/local/lib/node_modules",                                 // Node.js 全局依赖路径
        CHECK_CONFIG: $store.get('CHECK_CONFIG', 'string'),                       // 自定义 toml 配置文件路径，如 /ql/data/config/config.toml     
    },
    cb(data, error) {
        error ? console.error(error) : console.log(data);
    },
});
