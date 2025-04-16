import * as anchor from "@coral-xyz/anchor";
import * as web3 from "@solana/web3.js";
// Client
console.log("My address:", program.provider.publicKey.toString());
const balance = await program.provider.connection.getBalance(program.provider.publicKey);
console.log(`My balance: ${balance / web3.LAMPORTS_PER_SOL} SOL`);

console.log("Program address:", program.programId.toString());

import { PublicKey } from "@solana/web3.js";
import type { Pda } from "../target/types/pda";

// Configure the client to use the local cluster
anchor.setProvider(anchor.AnchorProvider.env());

const program = anchor.workspace.Pda as anchor.Program<Pda>;


const [wishPda, bump] = PublicKey.findProgramAddressSync(
  [Buffer.from("wish"), program.provider.publicKey.toBuffer()],
  program.programId
);

console.log("Wish PDA:", wishPda.toString())

const wishAccount = await program.account.wishAccount.fetch(wishPda);
console.log("Wish:", wishAccount.wish);