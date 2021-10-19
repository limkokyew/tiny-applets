import random
from objects import Attribute


def round_interval(value, min_value=0, max_value=100):
    return max(min_value, min(max_value, value))

def get_follow_up(user, target):
    user_as = user.get_attack_speed()
    target_as = target.get_attack_speed()
    
    print(f"{user} has {user_as} attack speed")
    print(f"{target} has {target_as} attack speed")

    if user_as - target_as >= 4:
        return user
    elif target_as - user_as >= 4:
        return target
    else:
        return None

def roll_hit_crit(unit, target):
    is_hit = False
    is_crit = False

    rn = sum([random.randint(0, 100) for _ in range(2)]) / 2
    if rn <= unit.get_hit() - target.get_avoid():
        is_hit = True
        crit_rn = random.randint(1, 100)
        if crit_rn <= unit.get_crit() - target.get_crit_avoid():
            is_crit = True
    
    return is_hit, is_crit

def can_attack(unit, distance):
    return unit.weapon is not None and distance in list(range(*tuple(sum(x) for x in zip(unit.weapon.w_range, (0, 1)))))

def get_combat_order(user, target, distance):
    target_retaliation = can_attack(target, distance)
    follow_up = get_follow_up(user, target)
    user_attack_per_round = 2 if user.weapon.brave else 1

    vantage = target.has_skill("Vantage")
    desperation = user.has_skill("Desperation")
    
    if target_retaliation:
        if vantage and target.stats["hp"] <= target.maxHP // 2:
            print(f"{target} activated Vantage!")
            rounds = [target]
            if follow_up == user:
                rounds += ([user] * user_attack_per_round) * 2
            elif follow_up == target:
                rounds += [user] * user_attack_per_round + [target]
            else:
                rounds += [user] * user_attack_per_round
        else:
            rounds = [user] * user_attack_per_round
            if follow_up == user:
                if desperation:
                    rounds += [user] * user_attack_per_round + [target]
                else:
                    rounds += [target] + [user] * user_attack_per_round
            elif follow_up == target:
                rounds += [target] * 2
            else:
                rounds += [target]
    else:
        rounds = [user] * user_attack_per_round
        if follow_up == user:
            rounds += [user] * user_attack_per_round
    
    return rounds


def combat(user, target, distance):
    combat_order = get_combat_order(user, target, distance)
    print(f"Combat order: {combat_order}", end="\n\n")

    user_hp = user.get_stat(Attribute.HP)
    user_mt = user.get_mt(initiate=True) - target.get_prt() if not user.weapon.magic else user.get_mt(initiate=True) - target.get_res()
    user_hit = round_interval(user.get_hit() - target.get_avoid())
    user_crit = round_interval(user.get_crit() - target.get_crit_avoid())
    
    target_hp = target.get_stat(Attribute.HP)
    target_mt = target.get_mt(counter=True) - user.get_prt() if not target.weapon.magic else target.get_mt(counter=True) - user.get_res()
    target_hit = round_interval(target.get_hit() - user.get_avoid())
    target_crit = round_interval(target.get_crit() - user.get_crit_avoid())
    
    print(f"{user} - HP: {user_hp}, Mt: {user_mt}, Hit: {user_hit}, Crit: {user_crit}")
    
    if can_attack(target, distance):
        print(f"{target} - HP: {target_hp}, Mt: {target_mt}, Hit: {target_hit}, Crit: {target_crit}", end="\n\n")
    else:
        print(f"{target} - HP: {target_hp}, Mt: -, Hit: -, Crit: -")
    
    combat_round = 1
    for unit in combat_order:
        print(f"-- ROUND {combat_round} --")
        combat_target = target if unit == user else user
        ct_initiate = True if combat_target == target else False
        ct_counter = True if combat_target == user else False
    
        hit, crit = roll_hit_crit(unit, combat_target)
        mt = (unit.get_mt(initiate=ct_initiate, counter=ct_counter) - combat_target.get_prt() if not unit.weapon.magic
              else unit.get_mt(initiate=ct_initiate, counter=ct_counter) - combat_target.get_res())
        if hit:
            if crit:
                mt *= 3
                crit_quote = unit.get_crit_quote()
                if crit_quote:
                    print(f"{unit}: \"{crit_quote}\"")
                print(f"{unit} dealt {mt} damage (Critical Hit)", end="")
            else:
                print(f"{unit} dealt {mt} damage", end="")
            combat_target.damage(mt)
            combat_target_hp = combat_target.get_stat(Attribute.HP)
            if combat_target_hp <= 0:
                print(f"\n{combat_target} was killed!")
                return
            else:
                print(f": {combat_target} has {combat_target_hp} HP remaining!")
        else:
            print(f"{unit} missed!")
        
        combat_round += 1


