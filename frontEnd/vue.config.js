module.exports = {
    devServer: {
        overlay: {
            warnings: false,
            errors: false
        },
        proxy: {
            '/': {
                // target: 'https://10.38.90.22:5013',  // 后台接口域名
                target: 'https://127.0.0.1:5013',  // 后台接口域名
                secure: false,  // 如果是https接口，需要配置这个参数
                changeOrigin: true,  //是否跨域
                pathRewrite:{
                    '^/':'/'
                }
            },
        },
        host: 'localhost',
    },
    lintOnSave: false,
    // publicPath :process.env.NODE_ENV === 'production' ? './static' : '/'
    publicPath: './static'
}
