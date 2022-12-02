// @grant nodejs
let shname = $env.SHNAME;
console.log(`⏳ 开始执行 ${shname}`);
$exec(`bash ${shname}`, {
    cwd: 'script/Shell/checkinpanel',
    timeout: 0,
    // prettier-ignore
    env: {
        ENV_PATH: $store.get('ENV_PATH', 'string'),                               // 自定义 .env 配置文件路径，如 /usr/local/app/script/Lists/.env
    },
    cb(data, error) {
        error ? console.error(error) : console.log(data);
    },
});
