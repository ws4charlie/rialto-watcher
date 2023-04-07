from ..chains import *
from .config import *

## Rialto bridges in mainnets
## BSC ========================================================================================================
Rialto_BSC_mainnet_src = ChainConfig("Findora", BRIDGE_BSC_mainnet_src_created, Confirm_FRA,
                                    ChainID_FRA_mainnet, URL_FRA_mainnet, ID_FRA, BRIDGE_BSC_mainnet_src, HANDLE_BSC_mainnet_src,
                                    ChainID_BSC_mainnet, URL_BSC_mainnet, ID_BSC, BRIDGE_BSC_mainnet_dst, HANDLE_BSC_mainnet_dst)

Rialto_BSC_mainnet_dst = ChainConfig("BSC", BRIDGE_BSC_mainnet_dst_created, Confirm_BSC,
                                ChainID_BSC_mainnet, URL_BSC_mainnet, ID_BSC, BRIDGE_BSC_mainnet_dst, HANDLE_BSC_mainnet_dst,
                                ChainID_FRA_mainnet, URL_FRA_mainnet, ID_FRA, BRIDGE_BSC_mainnet_src, HANDLE_BSC_mainnet_src)

## ETH ========================================================================================================
Rialto_ETH_mainnet_src = ChainConfig("Findora", BRIDGE_ETH_mainnet_src_created, Confirm_FRA,
                                    ChainID_FRA_mainnet, URL_FRA_mainnet, ID_FRA, BRIDGE_ETH_mainnet_src, HANDLE_ETH_mainnet_src,
                                    ChainID_ETH_mainnet, URL_ETH_mainnet, ID_ETH, BRIDGE_ETH_mainnet_dst, HANDLE_ETH_mainnet_dst)

Rialto_ETH_mainnet_dst = ChainConfig("ETH", BRIDGE_ETH_mainnet_dst_created, Confirm_ETH,
                                ChainID_ETH_mainnet, URL_ETH_mainnet, ID_ETH, BRIDGE_ETH_mainnet_dst, HANDLE_ETH_mainnet_dst,
                                ChainID_FRA_mainnet, URL_FRA_mainnet, ID_FRA, BRIDGE_ETH_mainnet_src, HANDLE_ETH_mainnet_src)

## Polygon ====================================================================================================
Rialto_PLY_mainnet_src = ChainConfig("Findora", BRIDGE_PLY_mainnet_src_created, Confirm_FRA,
                                    ChainID_FRA_mainnet, URL_FRA_mainnet, ID_FRA, BRIDGE_PLY_mainnet_src, HANDLE_PLY_mainnet_src,
                                    ChainID_PLY_mainnet, URL_PLY_mainnet, ID_PLY, BRIDGE_PLY_mainnet_dst, HANDLE_PLY_mainnet_dst)

Rialto_PLY_mainnet_dst = ChainConfig("Polygon", BRIDGE_PLY_mainnet_dst_created, Confirm_PLY,
                                ChainID_PLY_mainnet, URL_PLY_mainnet, ID_PLY, BRIDGE_PLY_mainnet_dst, HANDLE_PLY_mainnet_dst,
                                ChainID_FRA_mainnet, URL_FRA_mainnet, ID_FRA, BRIDGE_PLY_mainnet_src, HANDLE_PLY_mainnet_src)

## FTM ========================================================================================================
Rialto_FTM_mainnet_src = ChainConfig("Findora", BRIDGE_FTM_mainnet_src_created, Confirm_FRA,
                                    ChainID_FRA_mainnet, URL_FRA_mainnet, ID_FRA, BRIDGE_FTM_mainnet_src, HANDLE_FTM_mainnet_src,
                                    ChainID_FTM_mainnet, URL_FTM_mainnet, ID_FTM, BRIDGE_FTM_mainnet_dst, HANDLE_FTM_mainnet_dst)

Rialto_FTM_mainnet_dst = ChainConfig("FTM", BRIDGE_FTM_mainnet_dst_created, Confirm_FTM,
                                ChainID_FTM_mainnet, URL_FRA_mainnet, ID_FRA, BRIDGE_FTM_mainnet_src, HANDLE_FTM_mainnet_src,
                                ChainID_FRA_mainnet, URL_FTM_mainnet, ID_FTM, BRIDGE_FTM_mainnet_dst, HANDLE_FTM_mainnet_dst)



## Rialto bridges in testnets
## BSC Testnet =================================================================================================
Rialto_BSC_testnet_src = ChainConfig("Anvil", BRIDGE_BSC_testnet_src_created, Confirm_FRA,
                            ChainID_FRA_testnet, URL_FRA_testnet, ID_FRA, BRIDGE_BSC_testnet_src, HANDLE_BSC_testnet_src,
                            ChainID_BSC_testnet, URL_BSC_testnet, ID_BSC, BRIDGE_BSC_testnet_dst, HANDLE_BSC_testnet_dst)

Rialto_BSC_testnet_dst = ChainConfig("BSC-Testnet", BRIDGE_BSC_testnet_dst_created, Confirm_BSC,
                            ChainID_BSC_testnet, URL_BSC_testnet, ID_BSC, BRIDGE_BSC_testnet_dst, HANDLE_BSC_testnet_dst,
                            ChainID_FRA_testnet, URL_FRA_testnet, ID_FRA, BRIDGE_BSC_testnet_src, HANDLE_BSC_testnet_src)

## ETH Testnet =================================================================================================
Rialto_ETH_testnet_src = ChainConfig("Anvil", BRIDGE_ETH_testnet_src_created, Confirm_FRA,
                            ChainID_FRA_testnet, URL_FRA_testnet, ID_FRA, BRIDGE_ETH_testnet_src, HANDLE_ETH_testnet_src,
                            ChainID_ETH_testnet, URL_ETH_testnet, ID_ETH, BRIDGE_ETH_testnet_dst, HANDLE_ETH_testnet_dst)

Rialto_ETH_testnet_dst = ChainConfig("Ropsten", BRIDGE_ETH_testnet_dst_created, Confirm_ETH,
                            ChainID_ETH_testnet, URL_ETH_testnet, ID_ETH, BRIDGE_ETH_testnet_dst, HANDLE_ETH_testnet_dst,
                            ChainID_FRA_testnet, URL_FRA_testnet, ID_FRA, BRIDGE_ETH_testnet_src, HANDLE_ETH_testnet_src)

## Polygon Testnet ============================================================================================
Rialto_PLY_testnet_src = ChainConfig("Anvil", BRIDGE_PLY_testnet_src_created, Confirm_FRA,
                            ChainID_FRA_testnet, URL_FRA_testnet, ID_FRA, BRIDGE_PLY_testnet_src, HANDLE_PLY_testnet_src,
                            ChainID_PLY_testnet, URL_PLY_testnet, ID_PLY, BRIDGE_PLY_testnet_dst, HANDLE_PLY_testnet_dst)

Rialto_PLY_testnet_dst = ChainConfig("Mumbai", BRIDGE_PLY_testnet_dst_created, Confirm_PLY,
                            ChainID_PLY_testnet, URL_PLY_testnet, ID_PLY, BRIDGE_PLY_testnet_dst, HANDLE_PLY_testnet_dst,
                            ChainID_FRA_testnet, URL_FRA_testnet, ID_FRA, BRIDGE_PLY_testnet_src, HANDLE_PLY_testnet_src)

## FTM Testnet =================================================================================================
Rialto_FTM_testnet_src = ChainConfig("Anvil", BRIDGE_FTM_testnet_src_created, Confirm_FRA,
                            ChainID_FRA_testnet, URL_FRA_testnet, ID_FRA, BRIDGE_FTM_testnet_src, HANDLE_FTM_testnet_src,
                            ChainID_FTM_testnet, URL_FTM_testnet, ID_FTM, BRIDGE_FTM_testnet_dst, HANDLE_FTM_testnet_dst)

Rialto_FTM_testnet_dst = ChainConfig("FTM-Testnet", BRIDGE_FTM_testnet_dst_created, Confirm_FTM,
                            ChainID_FTM_testnet, URL_FTM_testnet, ID_FTM, BRIDGE_FTM_testnet_dst, HANDLE_FTM_testnet_dst,
                            ChainID_FRA_testnet, URL_FRA_testnet, ID_FRA, BRIDGE_FTM_testnet_src, HANDLE_FTM_testnet_src)


# Config of rialtos
CHAINS = {
    "Mainnet": {
        "BSC": ( Rialto_BSC_mainnet_src, Rialto_BSC_mainnet_dst ),
        "ETH": ( Rialto_ETH_mainnet_src, Rialto_ETH_mainnet_dst ),
        "PLY": ( Rialto_PLY_mainnet_src, Rialto_PLY_mainnet_dst ),
        "FTM": ( Rialto_FTM_mainnet_src, Rialto_FTM_mainnet_dst )
    },

    "Testnet": {
        "BSC": ( Rialto_BSC_testnet_src, Rialto_BSC_testnet_dst ),
        "ETH": ( Rialto_ETH_testnet_src, Rialto_ETH_testnet_dst ),
        "PLY": ( Rialto_PLY_testnet_src, Rialto_PLY_testnet_dst ),
        "FTM": ( Rialto_FTM_testnet_src, Rialto_FTM_testnet_dst )
    }
}


def get_chain(bridge, testnet):
    try:
        if testnet:
            return CHAINS['Testnet'][bridge]
        else:
            return CHAINS['Mainnet'][bridge]

    except:
        print("{}network not found: {}{}".format(FAIL, bridge, ENDC))
        exit(-1)
