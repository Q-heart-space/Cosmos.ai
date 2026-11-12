# [方法] FDE 接入五章骨架

> **版本**：v1.0 | **类型**：📋 | **日期**：2026-11-12 | **状态**：活跃
> **判据**：每章附**仓内可复算命令**；6 项验收全为命令

## 🛑 本件边界（先读）

1. **本件是方法论骨架**：🛑 **不含对外承诺、不含商务条款、不含任何客户数据/案例**。
2. 承诺性表述、验收口径的商务解释、真实案例 ⇒ 属**服务交付面**（`deliverables/` 与客户合同），**不在本件**。
3. 命令以**参数占位**（`<域>`／`<组织>`／`<包目录>`）给出，具体值由接入方填。

---

## 一、五章骨架（每章：输入 → 判据 → 失败处置）

### S1 定组织身份

| 项 | 内容 |
|:--|:--|
| **输入** | `<域>/<组织>/_org.json`（组织键与业务域） |
| **动作** | 把组织登记进**唯一组织清单** |
| **判据** | `python scripts/org_packaging_check.py` — 组织键须 ∈ `**你的组织清单文件**中的组织键列表` |
| **失败处置** | P0「未登记」⇒ 先登记再建包；🛑 不得绕过判据 |

### S2 选场景实例

| 项 | 内容 |
|:--|:--|
| **输入** | `你的场景清单（每空间一份）`（`scenario_id`／`space`／`adopted_at`／指针） |
| **动作** | 确认采用的场景，并把场景挂到本体 ObjectType 上 |
| **判据** | `python scripts/instance_mapping_check.py` — 类型→实例挂接成立；**跨空间项为「未判定」** |
| **失败处置** | 键未定 ⇒ 走 S3 的 `key_source` 声明（键值运行期由配置提供）；跨空间 ⇒ 标未判定 |

### S3 连技能数据源

| 项 | 内容 |
|:--|:--|
| **输入** | `各技能的配置文件`（ERP `form_id`／CRM token／简道云 `app_id`／渠道 `topic_id`） |
| **动作** | 数据源接到对应技能；**凭据只存客户侧 config** |
| **判据** | `python scripts/release_face_classifier_check.py`（能力面可分类）＋ `python scripts/skill_env_var_contamination_check.py`（环境变量名未污染） |
| **失败处置** | 凭据缺失 ⇒ 该技能标「不可用」；🛑 不写死凭据到仓内 |

### S4 声明规则覆盖

| 项 | 内容 |
|:--|:--|
| **输入** | `你的规则覆盖清单（每空间一份）`（`rule_ref`／`override`／`decided_by`／`decided_at`） |
| **动作** | 客户对通用规则的例外，必须带**人类决定点** |
| **判据** | `python scripts/product_manifest_check.py`（`release_contract` 六段指针有效） |
| **失败处置** | 缺 `decided_by/decided_at` ⇒ P0：例外不可无主 |

### S5 落品类规则

| 项 | 内容 |
|:--|:--|
| **输入** | `product-data-pipeline/category_mapping.md` ＋ `你的品类清单` |
| **动作** | 品类口径落到**客户配置**（品类规则以客户配置为唯一权威） |
| **判据** | `python scripts/org_packaging_check.py`（`acceptance` 全部为可复算命令） |
| **失败处置** | 口径冲突 ⇒ 按客户配置；🛑 不改本体默认口径 |

---

## 二、验收六项（全为命令·可复算）

| # | 验收项 | 命令 | 期望 |
|:--:|:--|:--|:--|
| A1 | 发布物无 L2 实例 | `python scripts/release_l2_instance_guard.py --root <包目录>` | rc=0 |
| A2 | 类型→实例挂接 | `python scripts/instance_mapping_check.py` | rc=0（跨空间项披露） |
| A3 | 发布面可分类 | `python scripts/release_face_classifier_check.py` | 未判定 0 |
| A4 | 组织声明合规 | `python scripts/org_packaging_check.py` | P0 0 |
| A5 | 发布包契约 | `python scripts/product_manifest_check.py` | PASS |
| A6 | 推送前全闸 | `python scripts/pre_push_gates.py` | 全绿 |

🛑 **不写「已完成」的项**：跨空间数据可达性——一律标**未判定**。

---

## 三、回滚（≤4 步）

1. 删除该组织的 `org_packaging.<域>-<组织>.json`；
2. 从 `**你的组织清单文件**中的组织键列表` 移除该 org；
3. `python scripts/org_packaging_check.py` 确认回到 P0 0；
4. `python scripts/pre_push_gates.py` 确认全绿。

---

## 四、本件自陈边界（🛑 不冒充）

| 项 | 状态 |
|:--|:--|
| 对外承诺/商务条款 | 🛑 **不在本件**（属服务交付面） |
| 真实案例 | 🛑 **不含**（案例 schema 与服务面另置） |
| 客户数据 | 🛑 **零含**（全部以 `<域>/<组织>` 占位） |
| 真实第二组织端到端 | 🟡 未验（仅结构演练：五章命令可执行＋未登记组织被拦） |