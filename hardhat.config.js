require("@nomicfoundation/hardhat-toolbox");
require("dotenv").config();

module.exports = {
  solidity: "0.8.20",
  networks: {
    okt: {
      url: "https://exchaintestrpc.okex.org", // OKT Chain testnet
      accounts: [process.env.PRIVATE_KEY], // Your wallet private key
    },
    sepolia: {
      url: "https://rpc.sepolia.org",
      accounts: [process.env.PRIVATE_KEY],
    },
  },
};