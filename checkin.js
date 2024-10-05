// @grant nodejs
let pyname = $env.PYNAME;
console.log(`⏳ 开始执行 ${pyname}`);
$exec(`python3 ${pyname}`, {
    cwd: 'script/Shell/checkinpanel',
    timeout: 0,
    // prettier-ignore
    env: {
        CHECK_CONFIG: $store.get('CHECK_CONFIG', 'string'),                       // 自定义 toml 配置文件路径，如 /usr/local/app/script/Lists/config.toml     
    },
    cb(data, error) {
        error ? console.error(error) : console.log(data);
    },
});
