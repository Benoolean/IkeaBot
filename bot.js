const Discord = require("discord.js");
const config = require("./authentication/config.json");
const fs = require('fs');

const prefix = config.prefix;
const bot = new Discord.Client();

bot.commands = new Discord.Collection();

fs.readdir('./commands/', (err, files) => {
    if (err)
        console.log(err);

    let command_files = files.filter(f => f.split('.').pop() === 'js');
    if (command_files <= 0) {
        console.log('No command files found.');
    }

    console.log('Loading ' + command_files.length + ' commands.');
    
    command_files.forEach((command, idx) => {
        let file = require('./commands/' + command);
        bot.commands.set(file.description.name, file);
        console.log('Command file ['+ (idx + 1) +'] ' + command + ' has been loaded');
    });
})

// bot login with auth token
bot.login(config.token);

// ready status function
bot.on("ready", () => {
    console.info('Logged in as ' + bot.user.tag + '!');
});

bot.on('message', message => {
    if (message.author.bot) return;
    
    let messageArray = message.content.split(/\s+/g);
    let command = messageArray[0];
    let args = messageArray.slice(1);

    if (!command.startsWith(prefix)) return;
    
    let command_module = bot.commands.get(command.slice(prefix.length));
    if (command_module) command_module.run(bot, message, args);
})
