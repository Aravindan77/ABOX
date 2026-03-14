'use client';

import { useReadContract, useWriteContract } from 'wagmi';
import BOUNTY_VAULT_ABI from '@/contracts/BountyVault.json';

const CONTRACT_ADDRESS = (process.env.NEXT_PUBLIC_BOUNTY_VAULT_ADDRESS || '0x0000000000000000000000000000000000000000') as `0x${string}`;

export function useBountyVaultRead(functionName: string, args?: unknown[]) {
    return useReadContract({
        address: CONTRACT_ADDRESS,
        abi: BOUNTY_VAULT_ABI,
        functionName,
        args,
    });
}

export function useBountyVaultWrite() {
    return useWriteContract();
}

export { CONTRACT_ADDRESS, BOUNTY_VAULT_ABI };
