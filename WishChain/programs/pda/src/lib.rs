use anchor_lang::prelude::*;

declare_id!("3JM2D4v3NZL97EPG9u5ViEEp2ZXhkWad1ab56jC7d8vg");

#[program]
pub mod pda {
    use super::*;

    // ctx: Context<Create> provides access to accounts in the Create struct
    pub fn awish(ctx: Context<CreateWish>, title: String) -> Result<()> {
        msg!("Create Wish {}", title);
        let account_data = &mut ctx.accounts.wish_account;
        // selects the user field to the public key of the user account
        account_data.user = ctx.accounts.user.key();
        account_data.wish = title;
        account_data.bump = ctx.bumps.wish_account;
        Ok(())
    }

    pub fn updatewish(ctx: Context<UpdateWish>, wish: String) -> Result<()> {
        msg!("Update Wish: {}", wish);
        let account_data = &mut ctx.accounts.wish_account;
        account_data.wish = wish;
        Ok(())
    }

    pub fn deletewish(_ctx: Context<DeleteWish>) -> Result<()> {
        // Needs no extra context as the close constraint in the Delete struct handles the account closing
        msg!("Delete Wish");
        Ok(())
    }
}

#[derive(Accounts)]
pub struct CreateWish<'info> {
    // Mutatble because we pay for our own account (kinda)
    #[account(mut)]
    pub user: Signer<'info>,
    #[account (
        // Creates the account during instruction execution
        init,
        // seed and bump together define an account's address as a Program Derived Address
        // a fixed string is the first seed and the public key of the user as the second seed
        seeds = [b"wish", user.key().as_ref()],
        // tells anchor to find and use hte correct bump seed
        bump,
        // Identifies who pays for the new account creation
        payer = user,
        // Allocates the required bytes for the account's data
        // 8 for anchor account discriminator
        // 32 bytes for the user public key
        // PDA bump seed takes one byte in u8
        space = 8 + 32 + 4 + "When I wish upon a star".len() + 1
    )]
    pub wish_account: Account<'info, WishAccount>,
    // Needed for account creation, init calls the System Program to create a new account
    // using the specified space and changes the owner to the current program (behind the scenes)
    pub system_program: Program<'info, System>,
}

#[derive(Accounts)]
pub struct UpdateWish<'info> {
    #[account(mut)]
    pub user: Signer<'info>,

    #[account (
        mut,
        seeds = [b"wish", user.key().as_ref()],
        bump = wish_account.bump,
        realloc = 8 + 32 + 4 + "When I wish upon a star".len() + 1,
        realloc::payer = user,
        realloc::zero = true,
    )]
    pub wish_account: Account<'info, WishAccount>,
    pub system_program: Program<'info, System>,
}

#[derive(Accounts)]
pub struct DeleteWish<'info> {
    #[account(mut)]
    pub user: Signer<'info>,

    #[account (
        mut,
        seeds = [b"wish", user.key().as_ref()],
        bump = wish_account.bump,
        close = user,
    )]
    pub wish_account: Account<'info, WishAccount>,
}

#[account]
pub struct WishAccount {
    pub user: Pubkey,
    pub wish: String,
    pub bump: u8,
}
