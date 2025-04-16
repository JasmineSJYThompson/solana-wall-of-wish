import * as anchor from "@coral-xyz/anchor";
import * as web3 from "@solana/web3.js";

import { PublicKey } from "@solana/web3.js";
import type { Pda } from "../target/types/pda";

console.log("Public key:", PublicKey);

describe("pda", () => {
  // Configure the client to use the local cluster
  anchor.setProvider(anchor.AnchorProvider.env());

  const program = anchor.workspace.Pda as anchor.Program<Pda>;
  
  const program = program;
  const wallet = pg.wallet;

  const [wishPda, wishBump] = PublicKey.findProgramAddressSync(
    [Buffer.from("wish"), wallet.publicKey.toBuffer()],
    program.programId,
  );

  it("Create Wish Account", async () => {
    const wish = "I want some bitcoin!";
    const transactionSignature = await program.methods
      .awish(wish)
      .accounts({
        wishAccount: wishPda,
      })
      .rpc({ commitment: "confirmed" });

    const wishAccount = await program.account.wishAccount.fetch(
      wishPda,
      "confirmed",
    );

    console.log(JSON.stringify(wishAccount, null, 2));
    console.log(
      "Transaction Signature:",
      `https://solana.fm/tx/${transactionSignature}?cluster=devnet-solana`,
    );
  });

  it("Update Wish Account", async () => {
    const wish = "I want some SOL!";
    const transactionSignature = await program.methods
      .updatewish(wish)
      .accounts({
        wishAccount: wishPda,
      })
      .rpc({ commitment: "confirmed" });

    const wishAccount = await program.account.wishAccount.fetch(
      wishPda,
      "confirmed",
    );

    console.log(JSON.stringify(wishAccount, null, 2));
    console.log(
      "Transaction Signature:",
      `https://solana.fm/tx/${transactionSignature}?cluster=devnet-solana`,
    );
  });

  /**it("Delete Wish Account", async () => {
    const transactionSignature = await program.methods
      .deletewish()
      .accounts({
        wishAccount: wishPda,
      })
      .rpc({ commitment: "confirmed" });

    const wishAccount = await program.account.wishAccount.fetchNullable(
      wishPda,
      "confirmed",
    );

    console.log("Expect Null:", JSON.stringify(wishAccount, null, 2));
    console.log(
      "Transaction Signature:",
      `https://solana.fm/tx/${transactionSignature}?cluster=devnet-solana`,
    );
  });*/
});
