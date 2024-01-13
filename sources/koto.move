// Copyright (c) Studio Mirai, LLC
// SPDX-License-Identifier: Apache-2.0

module koto::koto {
    use std::option;
    
    use sui::coin::{Self, Coin, TreasuryCap};
    use sui::transfer;
    use sui::tx_context::{Self, TxContext};

    struct KOTO has drop {}

    #[allow(unused_function)]
    fun init(
        otw: KOTO,
        ctx: &mut TxContext,
    ) {
        let (treasury_cap, metadata) = coin::create_currency<KOTO>(
            otw,
            0,
            b"KOTO",
            b"KOTO",
            b"KOTO is the utility token that powers the Studio Mirai ecosystem.",
            option::none(),
            ctx,
        );

        transfer::public_freeze_object(metadata);
        transfer::public_transfer(treasury_cap, tx_context::sender(ctx))
    }

    public entry fun mint(
        treasury_cap: &mut TreasuryCap<KOTO>,
        amount: u64,
        recipient: address,
        ctx: &mut TxContext,
    ) {
        coin::mint_and_transfer(treasury_cap, amount, recipient, ctx)
    }

    public entry fun burn(
        treasury_cap: &mut TreasuryCap<KOTO>,
        coin: Coin<KOTO>,
    ) {
        coin::burn(treasury_cap, coin);
    }
}
