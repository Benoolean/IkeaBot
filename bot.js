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
                    category = (idx + 1) + "|" + line.substring(4);
                    console.log(category);

                    category_arr.push(category);
                }
            });

            // getting the category
            var category_index = randomInt(0, category_arr.length);
            var category = category_arr[category_index];
            var next_category = (category_index < category_arr.length - 1) ? category_arr[category_index + 1] : null;

            // getting the product

            // regex for getting all char before the : char
            var min_index = category.match(/^[^|]+/);

            // Since there is a space between each category, we remove 2 from the max_index
            var max_index = (next_category != null) ? next_category.match(/^[^|]+/) - 2 : -1;  

            // resulting product
            var result_index = randomInt(parseInt(min_index) + 1, (max_index != -1 ? parseInt(max_index) : file.length - 2));
            
            // console.log('======');
            // console.log('DEBUG:');
            // console.log('Cat: ' + category + ' CatIdx: ' + category_index + ' CatLen: ' + category_arr.length);
            // console.log('Min: ' + min_index + ' Max: ' + max_index);
            // console.log('Result: ' + result_index);
            // console.log('======');

            
            file.forEach((line, index) => {
                if (result_index == index) {
                    console.log(category.match(/[^|]*$/) + "| " + line);

                    msg.channel.send(category.match(/[^|]*$/) + " | " + line);
                    return;
                }   
            });
        }
    }
});