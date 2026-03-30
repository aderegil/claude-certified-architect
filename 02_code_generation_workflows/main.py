# main.py - Validates Claude Code workspace configuration
import json
import os

from config import CYAN, GREEN, YELLOW, RED, DIM, BOLD, RESET


def check_claude_md():
    """Check that project-level CLAUDE.md exists and uses @import."""
    path = os.path.join(os.path.dirname(__file__), "CLAUDE.md")
    if not os.path.exists(path):
        result = (False, "CLAUDE.md not found at project root")
        return result
    with open(path, "r") as f:
        content = f.read()
    if "@import" not in content:
        result = (False, "CLAUDE.md exists but does not use @import")
        return result
    result = (True, "CLAUDE.md exists with @import")
    return result


def check_directory_claude_md():
    """Check that directory-level CLAUDE.md exists in app/."""
    path = os.path.join(os.path.dirname(__file__), "app", "CLAUDE.md")
    if not os.path.exists(path):
        result = (False, "app/CLAUDE.md not found (directory-level)")
        return result
    result = (True, "app/CLAUDE.md exists (directory-level)")
    return result


def check_path_rules():
    """Check .claude/rules/ has files with YAML frontmatter glob patterns."""
    rules_dir = os.path.join(os.path.dirname(__file__), ".claude", "rules")
    if not os.path.isdir(rules_dir):
        result = (False, ".claude/rules/ directory not found")
        return result

    rule_files = [f for f in os.listdir(rules_dir) if f.endswith(".md")]
    if not rule_files:
        result = (False, ".claude/rules/ exists but has no .md files")
        return result

    has_glob = False
    for rule_file in rule_files:
        filepath = os.path.join(rules_dir, rule_file)
        with open(filepath, "r") as f:
            content = f.read()
        if "paths:" in content and ("**/" in content or "*." in content):
            has_glob = True
            break

    if not has_glob:
        msg = f"Found {len(rule_files)} rule file(s) but none have glob patterns in paths:"
        result = (False, msg)
        return result

    result = (True, f"Found {len(rule_files)} rule file(s) with glob patterns")
    return result


def check_custom_skill():
    """Check .claude/commands/ has a skill with context:fork."""
    commands_dir = os.path.join(os.path.dirname(__file__), ".claude", "commands")
    if not os.path.isdir(commands_dir):
        result = (False, ".claude/commands/ directory not found")
        return result

    skill_files = [f for f in os.listdir(commands_dir) if f.endswith(".md")]
    if not skill_files:
        result = (False, ".claude/commands/ exists but has no .md files")
        return result

    has_fork = False
    for skill_file in skill_files:
        filepath = os.path.join(commands_dir, skill_file)
        with open(filepath, "r") as f:
            content = f.read()
        if "context:fork" in content or "context: fork" in content:
            has_fork = True
            break

    if not has_fork:
        msg = f"Found {len(skill_files)} skill(s) but none use context:fork"
        result = (False, msg)
        return result

    result = (True, f"Found {len(skill_files)} skill(s) with context:fork")
    return result


def check_mcp_config():
    """Check .mcp.json exists with env var expansion and inventory_server.py is present."""
    # Verify custom server file exists
    server_path = os.path.join(os.path.dirname(__file__), "mcp_server", "inventory_server.py")
    if not os.path.exists(server_path):
        result = (False, "mcp_server/inventory_server.py not found — custom MCP server missing")
        return result

    path = os.path.join(os.path.dirname(__file__), ".mcp.json")
    if not os.path.exists(path):
        result = (False, ".mcp.json not found")
        return result

    with open(path, "r") as f:
        content = f.read()

    try:
        config = json.loads(content)
    except json.JSONDecodeError:
        result = (False, ".mcp.json exists but is not valid JSON")
        return result

    if "mcpServers" not in config:
        result = (False, ".mcp.json missing mcpServers key")
        return result

    servers = config["mcpServers"]
    if "${" not in content:
        result = (False, ".mcp.json exists but does not use ${ENV_VAR} expansion")
        return result

    server_count = len(servers)
    result = (True, f".mcp.json configured with {server_count} server(s) and env var expansion")
    return result


def check_scratchpad():
    """Check scratch.md exists with structured findings."""
    path = os.path.join(os.path.dirname(__file__), "scratch.md")
    if not os.path.exists(path):
        result = (False, "scratch.md not found")
        return result

    with open(path, "r") as f:
        content = f.read()

    if len(content.strip()) < 10:
        result = (False, "scratch.md exists but appears empty")
        return result

    result = (True, "scratch.md exists with content")
    return result


def run_all_checks():
    """Run all validation checks and display results."""
    checks = [
        ("CLAUDE.md with @import", check_claude_md),
        ("Directory-level CLAUDE.md", check_directory_claude_md),
        ("Path-specific rules", check_path_rules),
        ("Custom skill (context:fork)", check_custom_skill),
        ("MCP server config", check_mcp_config),
        ("Context persistence (scratch.md)", check_scratchpad),
    ]

    print(f"\n{BOLD}Workspace Configuration Checks{RESET}\n")

    passed = 0
    total = len(checks)

    for name, check_fn in checks:
        ok, message = check_fn()
        if ok:
            print(f"  {GREEN}✓ {name}{RESET}")
            print(f"    {DIM}{message}{RESET}")
            passed += 1
        else:
            print(f"  {RED}✗ {name}{RESET}")
            print(f"    {DIM}{message}{RESET}")

    print(f"\n{BOLD}{passed}/{total} checks passed{RESET}")
    if passed == total:
        print(f"{GREEN}All checks passed! Workspace is fully configured.{RESET}")
    else:
        print(f"{YELLOW}Follow the README to complete the remaining configuration.{RESET}")
    print()


# --- Interactive mode ---

def clear_screen():
    os.system("cls" if os.name == "nt" else "clear")


def show_menu():
    print(f"{BOLD}Lab 02 — Code Generation with Claude Code{RESET}\n")
    print(f"  {DIM}1. Run all checks{RESET}")
    print(f"  {DIM}2. Check CLAUDE.md hierarchy{RESET}")
    print(f"  {DIM}3. Check path-specific rules{RESET}")
    print(f"  {DIM}4. Check custom skill{RESET}")
    print(f"  {DIM}5. Check MCP config{RESET}")
    print(f"  {DIM}6. Check context persistence{RESET}")
    print(f"  {DIM}c. Clear screen{RESET}")
    print(f"  {DIM}q. Quit{RESET}")
    print()


def main():
    clear_screen()
    show_menu()

    while True:
        user_input = input(f"{CYAN}Check > {RESET}").strip()

        if not user_input:
            continue
        if user_input.lower() in ("quit", "exit", "q"):
            break
        if user_input.lower() == "c":
            clear_screen()
            show_menu()
            continue

        if user_input == "1":
            run_all_checks()
        elif user_input == "2":
            ok1, msg1 = check_claude_md()
            ok2, msg2 = check_directory_claude_md()
            status1 = f"{GREEN}✓{RESET}" if ok1 else f"{RED}✗{RESET}"
            status2 = f"{GREEN}✓{RESET}" if ok2 else f"{RED}✗{RESET}"
            print(f"\n  {status1} Project-level: {DIM}{msg1}{RESET}")
            print(f"  {status2} Directory-level: {DIM}{msg2}{RESET}\n")
        elif user_input == "3":
            ok, msg = check_path_rules()
            status = f"{GREEN}✓{RESET}" if ok else f"{RED}✗{RESET}"
            print(f"\n  {status} {DIM}{msg}{RESET}\n")
        elif user_input == "4":
            ok, msg = check_custom_skill()
            status = f"{GREEN}✓{RESET}" if ok else f"{RED}✗{RESET}"
            print(f"\n  {status} {DIM}{msg}{RESET}\n")
        elif user_input == "5":
            ok, msg = check_mcp_config()
            status = f"{GREEN}✓{RESET}" if ok else f"{RED}✗{RESET}"
            print(f"\n  {status} {DIM}{msg}{RESET}\n")
        elif user_input == "6":
            ok, msg = check_scratchpad()
            status = f"{GREEN}✓{RESET}" if ok else f"{RED}✗{RESET}"
            print(f"\n  {status} {DIM}{msg}{RESET}\n")
        else:
            print(f"{DIM}Choose 1-6, c, or q.{RESET}")


if __name__ == "__main__":
    main()
