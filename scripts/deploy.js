const hre = require("hardhat");

async function main() {
  const [deployer] = await hre.ethers.getSigners();
  console.log("Deploying contracts with:", deployer.address);

  const GaslessTrading = await hre.ethers.getContractFactory("GaslessTrading");
  const entryPoint = "0x5FF137D4b0FDCD49DcA30c7CF57E578a026d2789"; // ERC-4337 EntryPoint (Sepolia)
  const okxDexRouter = "0x156ACd2bc5fC336D59BAAE602a2BD9b5e20D6672"; // Replace with OKX DEX Router address
  const initialOwner = deployer.address; // Set the deployer as the owner
  const gaslessTrading = await GaslessTrading.deploy(entryPoint, okxDexRouter, initialOwner);

  await gaslessTrading.deployed();
  console.log("GaslessTrading deployed to:", gaslessTrading.address);
}

main().catch((error) => {
  console.error(error);
  process.exitCode = 1;
});