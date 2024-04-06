// Copyright (c) Studio Mirai, Ltd.
// SPDX-License-Identifier: Apache-2.0

module koto::koto {

    use std::ascii::{Self};
    use std::option;
    
    use sui::coin::{Self, TreasuryCap};
    use sui::object::{Self, UID};
    use sui::transfer;
    use sui::tx_context::{Self, TxContext};
    use sui::url::{Self};

    struct KOTO has drop {}

    struct Gomi has key {
        id: UID,
        treasury_cap: TreasuryCap<KOTO>
    }

    #[allow(lint(freeze_wrapped))]
    fun init(
        witness: KOTO,
        ctx: &mut TxContext,
    ) {
        let (treasury_cap, metadata) = coin::create_currency(
            witness,
            0,
            b"KOTO",
            b"KOTO",
            b"The utility token of the Studio Mirai ecosystem.",
            option::some(url::new_unsafe(ascii::string(b"https://sm.xyz/images/koto.webp"))),
            ctx
        );

        coin::mint_and_transfer(&mut treasury_cap, 1_000_000_000_000, @sm_treasury, ctx);

        let gomi = Gomi { id: object::new(ctx), treasury_cap: treasury_cap };
        
        transfer::freeze_object(gomi);
        transfer::public_freeze_object(metadata);
    }
}