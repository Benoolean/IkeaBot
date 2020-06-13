require("dotenv").config();

const Discord = require("discord.js");
const bot = new Discord.Client();
const TOKEN = process.env.TOKEN;

function randomInt(min, max) {
    return Math.floor(Math.random() * (max - min)) + min; //The maximum is exclusive and the minimum is inclusive
}

bot.login(TOKEN);

bot.on("ready", () => {
    console.info(`Logged in as ${bot.user.tag}!`);
});

bot.on("message", msg => {
    if (msg.content === "debug") {
        if (msg.author.id === "318439813206376448") {
            msg.channel.send("Debugging Authenticated for: " + msg.author.username + "#" + msg.author.discriminator);

            var fs = require("fs");
            let file = fs.readFileSync("data/ikea_products.txt", "utf8").split(/\r?\n/);

            category_arr = [];
            file.forEach((line, idx) => {
                if(line.includes("URL")) {
                    product = (idx + 1) + ":" + line.substring(4);
                    console.log(product);

                    category_arr.append(product);
                }
            });

            var category = category_arr[randomInt(0, category_arr.length())];
            var next_category = category + 1;

            console.log(category, next_category);
        }
    }
});