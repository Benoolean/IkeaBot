require("dotenv").config();

const fs = require('fs');
const Discord = require("discord.js");
const bot = new Discord.Client();
const TOKEN = process.env.TOKEN;

// Command init
bot.commands = new Discord.Collection();

const commandFiles = fs.readdirSync('./commands').filter(file => file.endsWith('.js'));

for (const file of commandFiles) {
	const command = require(`./commands/${file}`);
	bot.commands.set(command.name, command);
}

bot.login(TOKEN);

bot.on("ready", () => {
    console.info('Logged in as' + bot.user.tag + '!');
});

bot.on("message", msg => {
    if (msg.content == "ikea-admin") {
        bot.commands.get('ikea-admin').execute(msg);
    }
});