'use client';

import { ConnectButton } from '@rainbow-me/rainbowkit';

export default function WalletConnectButton() {
    return (
        <ConnectButton.Custom>
            {({ account, chain, openAccountModal, openChainModal, openConnectModal, authenticationStatus, mounted }) => {
                const ready = mounted && authenticationStatus !== 'loading';
                const connected = ready && account && chain && (!authenticationStatus || authenticationStatus === 'authenticated');

                return (
                    <div
                        {...(!ready && {
                            'aria-hidden': true,
                            style: { opacity: 0, pointerEvents: 'none', userSelect: 'none' },
                        })}
                    >
                        {!connected ? (
                            <button
                                onClick={openConnectModal}
                                className="btn-neon text-sm font-semibold px-5 py-2.5"
                                id="connect-wallet-btn"
                            >
                                Connect Wallet
                            </button>
                        ) : chain?.unsupported ? (
                            <button
                                onClick={openChainModal}
                                className="px-4 py-2 text-sm font-semibold rounded-lg bg-danger/20 text-danger border border-danger/30 hover:bg-danger/30 transition-all"
                            >
                                Wrong Network
                            </button>
                        ) : (
                            <div className="flex items-center gap-2">
                                <button
                                    onClick={openChainModal}
                                    className="flex items-center gap-1.5 px-3 py-2 rounded-lg text-xs font-medium glass border border-white/10 hover:border-neon/20 transition-all"
                                >
                                    {chain.hasIcon && (
                                        <div className="w-3.5 h-3.5 rounded-full overflow-hidden">
                                            {chain.iconUrl && <img alt={chain.name} src={chain.iconUrl} className="w-full h-full" />}
                                        </div>
                                    )}
                                    <span className="text-text-secondary">{chain.name}</span>
                                </button>
                                <button
                                    onClick={openAccountModal}
                                    className="flex items-center gap-2 px-3 py-2 rounded-lg text-xs font-medium glass border border-neon/20 text-neon hover:bg-neon/10 transition-all"
                                    id="wallet-account-btn"
                                >
                                    {account.displayName}
                                </button>
                            </div>
                        )}
                    </div>
                );
            }}
        </ConnectButton.Custom>
    );
}
