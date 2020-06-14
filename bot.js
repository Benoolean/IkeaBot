require("dotenv").config();

const fs = require('fs');
const Discord = require("discord.js");
const config = require("./config.json");
const bot = new Discord.Client();
const command_prefix = config.prefix;

// Command init
bot.commands = new Discord.Collection();

const commandFiles = fs.readdirSync('./commands').filter(file => file.endsWith('.js'));

for (const file of commandFiles) {
	const command = require(`./commands/${file}`);
	bot.commands.set(command.name, command);
}

// bot login with auth token
bot.login(config.token);

// ready status function
bot.on("ready", () => {
    console.info('Logged in as' + bot.user.tag + '!');
});

// messaging center
bot.on("message", msg => {
    if (!msg.content.startsWith(command_prefix) || msg.author.bot) 
        return;

    if (msg.content.startsWith(command_prefix)){
        command = msg.content.substring(1).toLowerCase();

        if (command == "start") {
            bot.commands.get('ikea').execute(msg);
        }
        else if (command == "claim") {
            
        }
    }
});