
module.exports.run = async (bot, message, args) => {
    if (!message.author.bot) {
        
        let author = message.author;
        // remove the first command (including the prefix)
        message_args = message.content.split(' ').slice(1);
        console.log(message_args);

        if (message_args.length != 1) {
            message.channel.send(':no_entry_sign: Invalid arguments! :no_entry_sign:');
            return;
        }
        claim_answer =  message_args[0].toUpperCase();

        let product_data = JSON.parse(fs.readFileSync("data/ikea_products.txt", "utf8"));
        
        if (claim_answer == product_data.product_name) {
            message.channel.send(':clap: ' + author.displayAvatarURL({ dynamic: true }) + '. Congrats on your new IKEA product! :clap:');
        }
        else {
            message.channel.send(':rolling_eyes: ' + author.displayAvatarURL({ dynamic: true }) + '. Wrong name :rolling_eyes:');
        }

        return;
    }

    message.channel.send(':no_entry: Bots are not allowed to participate! :no_entry:');
}


module.exports.description = {
    name: 'claim'
}