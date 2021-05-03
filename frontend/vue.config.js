module.exports = {
    configureWebpack: {
        devtool: 'source-map'
    },
    css: {
        loaderOptions: {
            sass: {
                prependData: '\n          @import "@/scss/_variables.scss";\n        '
            }
        }
    },
    outputDir: '../backend/dist',
    assetsDir: 'static',
    devServer: {
        proxy: {
            '/api': {
                target: 'http://localhost:8112'
            },
        },
    }
}