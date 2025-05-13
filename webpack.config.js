const path = require("path");

module.exports = {
    entry: "./task11/static/js/main.js",
    output: {
        filename: "bundle.js",
        path: path.resolve(__dirname, "task11/static/dist"),
    },
    module: {
        rules: [{
                test: /\.js$/,
                exclude: /node_modules/,
                use: {
                    loader: "babel-loader",
                    options: {
                        presets: ["@babel/preset-env"],
                    },
                },
            },
            {
                test: /\.scss$/,
                use: ["style-loader", "css-loader", "sass-loader"],
            },
        ],
    },
    mode: "development",
    devtool: "source-map",
};