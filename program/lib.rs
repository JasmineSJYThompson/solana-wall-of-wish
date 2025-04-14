use anchor_lang::prelude::*;

declare_id!("Fg6PaFpoGXkYsidMpWTK6W2BeZ7FEfcYkg476zPFsLnS");

#[program]
pub mod wall_of_wish {
    use super::*;

    pub fn make_wish(ctx: Context<MakeWish>, title: String) -> Result<()> {
        let wish = &mut ctx.accounts.wish;
        wish.title = title;
        wish.author = ctx.accounts.author.key();
        wish.timestamp = Clock::get()?.unix_timestamp;
        Ok(())
    }
}

#[derive(Accounts)]
pub struct MakeWish<'info> {
    #[account(init, payer = author, space = 8 + 32 + 8 + 4 + 100)]
    pub wish: Account<'info, Wish>,
    #[account(mut)]
    pub author: Signer<'info>,
    pub system_program: Program<'info, System>,
}

#[account]
pub struct Wish {
    pub title: String,
    pub author: Pubkey,
    pub timestamp: i64,
} 