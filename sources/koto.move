// Copyright (c) Studio Mirai, LLC
// SPDX-License-Identifier: Apache-2.0

module koto::koto {

    use std::option;
    
    use sui::balance::{Self, Balance};
    use sui::coin::{Self, Coin, TreasuryCap};
    use sui::object::{Self, UID};
    use sui::transfer;
    use sui::tx_context::{Self, TxContext};

    struct KOTO has drop {}
    
    struct KotoTreasuryCap has key, store {
        id: UID,
    }

    struct KotoTreasury has key {
        id: UID,
        balance: Balance<KOTO>,
    }

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

        // Mint entire supply of KOTO.
        let supply = coin::mint_balance(&mut treasury_cap, 1_000_000_000_000);

        // Create treasury.
        let treasury = KotoTreasury {
            id: object::new(ctx),
            balance: supply,
        };

        transfer::share_object(treasury);
        transfer::public_freeze_object(metadata);
        transfer::public_freeze_object(treasury_cap);
    }
}
