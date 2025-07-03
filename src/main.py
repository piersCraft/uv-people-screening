from processors import fetch_ubo

def main():
    id: int = 60903
    owners = fetch_ubo.fetchBeneficialOwners(id)
    print(owners)

if __name__ == "__main__":
    main()
